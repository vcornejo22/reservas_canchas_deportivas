from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_socketio import SocketIO, emit
import eventlet
import requests
import logging

# Configura logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'clavecita'
# SocketIO
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/get_bookings/<int:field_id>/<int:start>/<int:end>')
def get_bookings(field_id, start, end):
    try:
        logger.debug(f"Received request - field_id: {field_id}, start: {start}, end: {end}")
        start_date = datetime.fromtimestamp(start/1000)
        end_date = datetime.fromtimestamp(end/1000)
        logger.debug(f"Converted dates - start_date: {start_date}, end_date: {end_date}")
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT booking_date, start_time, end_time, status
            FROM bookings
            WHERE field_id = %s AND booking_date BETWEEN %s AND %s
        ''', (field_id, start_date, end_date))
        
        bookings = cursor.fetchall()
        logger.debug(f"Found {len(bookings)} bookings")
        
        result = []
        for booking in bookings:
            booking_date = booking[0]  # datetime.date
            start_time = booking[1]    # datetime.timedelta
            end_time = booking[2]      # datetime.timedelta
            status = booking[3]        # string

            # Convertir timedelta a formato de hora (HH:MM:SS)
            start_time_str = str(datetime.min + start_time).split()[1]
            end_time_str = str(datetime.min + end_time).split()[1]

            booking_dict = {
                'start': f"{booking_date.strftime('%Y-%m-%d')} {start_time_str}",
                'end': f"{booking_date.strftime('%Y-%m-%d')} {end_time_str}",
                'status': status
            }
            result.append(booking_dict)

        logger.debug(f"result {result}")
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e: 
        logger.error(f"Error in get_bookings: {str(e)}")
        # Si hay una conexión abierta, ciérrala
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        return jsonify({'error': str(e)}), 500


@app.route('/create_booking', methods=['POST'])
def create_booking():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Please log in first'})

    data = request.json

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar disponibilidad
        cursor.execute('''
            SELECT id, status
            FROM bookings
            WHERE field_id = %s
            AND booking_date = %s
            AND ((start_time <= %s AND end_time > %s)
                OR (start_time < %s AND end_time >= %s))
        ''', (
            data['field_id'],
            data['date'],
            data['start_time'],
            data['start_time'],
            data['end_time'],
            data['end_time']
        ))
        r = cursor.fetchone()
        if r[1] != 'cancelled' or r is None:
            return jsonify({'success': False, 'error': 'Tiempo no disponible'})

        # Obtener precio
        cursor.execute(f'SELECT price_per_hour FROM fields WHERE id={data["field_id"]};')
        price_per_hour = cursor.fetchone()[0]
        data['user_id'] = session['user_id']
        data['total_price'] = float(price_per_hour)
        data['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Crear la reserva con el estado proporcionado
        cursor.execute('''
            INSERT INTO bookings (user_id, field_id, booking_date, start_time, end_time, status, total_price, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            session['user_id'],
            data['field_id'],
            data['date'],
            data['start_time'],
            data['end_time'],
            data.get('status', 'pending'),  # Usar el estado proporcionado o 'pending' por defecto
            data['total_price'],
            data['created_at']
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, name, price_per_hour FROM fields')
    fields = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', fields=fields)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']

        conn = get_db_connection()
        cursor = conn.cursor()
        # cursor = conn.cursor(dictionary=True)

        try:
            hashed_password = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password, email, phone) VALUES (%s, %s, %s, %s)',
                         (username, hashed_password, email, phone))
            conn.commit()
            flash('¡Registro exitoso! Por favor, inicie sesión..', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Error en el registro. Es posible que ya exista el nombre de usuario o el correo electrónico.', 'error')
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')

        cursor.close()
        conn.close()

    return render_template('login.html')

from datetime import datetime

@app.route('/payment_methods', methods=['GET'])
def payment_methods():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('''
        SELECT * FROM payment_methods
        WHERE user_id = %s
    ''', (session['user_id'],))

    payment_methods = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('payment_methods.html',
                         payment_methods=payment_methods,
                         current_year=datetime.now().year)

@app.route('/add_payment_method', methods=['GET', 'POST'])
def add_payment_method():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        card_number = request.form['card_number']
        card_holder = request.form['card_holder']
        expiration_month = request.form['expiration_month']
        expiration_year = request.form['expiration_year']
        card_type = request.form['card_type']
        last_four = card_number[-4:]  # Últimos 4 dígitos

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO payment_methods
                (user_id, card_number, card_holder, expiration_month,
                expiration_year, card_type, last_four)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (session['user_id'], card_number, card_holder,
                 expiration_month, expiration_year, card_type, last_four))

            conn.commit()
            flash('Método de pago agregado exitosamente', 'success')
            return redirect(url_for('payment_methods'))
        except Exception as e:
            conn.rollback()
            flash('Error al agregar método de pago', 'error')
        finally:
            cursor.close()
            conn.close()

    return render_template('payment_method_form.html',
                         current_year=datetime.now().year)

@app.route('/campos')
def campos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, name, price_per_hour FROM fields')
    fields = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('campos.html', fields=fields)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)


    # Get user's bookings
    cursor.execute('''
        SELECT
            b.id,
            b.booking_date,
            TIME_FORMAT(b.start_time, '%H:%i') as start_time,
            TIME_FORMAT(b.end_time, '%H:%i') as end_time,
            b.total_price,
            b.status,
            f.name as field_name
        FROM bookings b
        JOIN fields f ON b.field_id = f.id
        WHERE b.user_id = %s
        ORDER BY b.booking_date DESC, b.start_time DESC
    ''', (session['user_id'],))

    bookings = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('dashboard.html', bookings=bookings)

@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Verificar que la reserva pertenezca al usuario actual
    cursor.execute('''
        SELECT * FROM bookings
        WHERE id = %s AND user_id = %s AND status = 'pending'
    ''', (booking_id, session['user_id']))

    booking = cursor.fetchone()

    if booking:
        try:
            # Actualizar el estado de la reserva a 'cancelled'
            cursor.execute('''
                UPDATE bookings
                SET status = 'cancelled'
                WHERE id = %s
            ''', (booking_id,))

            conn.commit()
            flash('Reserva cancelada con éxito!', 'success')
        except Exception as e:
            conn.rollback()
            flash('Error al cancelar la reserva. Inténtalo de nuevo..', 'error')
    else:
        flash('Reserva no válida o no tienes permiso para cancelarla.', 'error')

    cursor.close()
    conn.close()

    return redirect(url_for('dashboard'))

@app.route('/confirm_booking/<int:booking_id>', methods=['POST'])
def confirm_booking(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Verificar que la reserva pertenezca al usuario actual
    cursor.execute('''
        SELECT * FROM bookings
        WHERE id = %s AND user_id = %s AND status = 'pending'
    ''', (booking_id, session['user_id']))

    booking = cursor.fetchone()

    if booking:
        try:
            # Actualizar el estado de la reserva a 'confirmed'
            cursor.execute('''
                UPDATE bookings
                SET status = 'confirmed'
                WHERE id = %s
            ''', (booking_id,))

            conn.commit()
            flash('¡Reserva confirmada con éxito!', 'success')
        except Exception as e:
            conn.rollback()
            flash('Error al confirmar la reserva. Inténtalo de nuevo.', 'error')
    else:
        flash('Reserva no válida o no tienes permiso para confirmarla.', 'error')

    cursor.close()
    conn.close()

    return redirect(url_for('dashboard'))

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        field_id = request.form['field_id']
        booking_date = request.form['booking_date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        payment_method_id = request.form['payment_method']

        # Calculate total price
        cursor.execute('SELECT price_per_hour FROM fields WHERE id = %s', (field_id,))
        field = cursor.fetchone()

        start_datetime = datetime.datetime.strptime(start_time, '%H:%M')
        end_datetime = datetime.datetime.strptime(end_time, '%H:%M')
        duration = (end_datetime - start_datetime).total_seconds() / 3600
        total_price = float(field['price_per_hour']) * duration

        try:
            # cursor.execute('''
            #     INSERT INTO bookings
            #     (user_id, field_id, booking_date, start_time, end_time, total_price)
            #     VALUES (%s, %s, %s, %s, %s, %s)
            # ''', (session['user_id'], field_id, booking_date, start_time, end_time, total_price))
            
            # En la ruta de crear reserva, actualiza la inserción:
            cursor.execute('''
                INSERT INTO bookings
                (user_id, field_id, booking_date, start_time, end_time,
                total_price, payment_method_id, payment_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending')
            ''', (session['user_id'], field_id, booking_date, start_time,
                end_time, total_price, payment_method_id))

            conn.commit()
            flash('Reserva realizada con éxito!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash('La reserva ha fallado. Inténtalo de nuevo..', 'error')

    # Get available fields
    cursor.execute('SELECT * FROM fields')
    fields = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('booking.html', fields=fields)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

## CHATBOT
@socketio.on('connect')
def handle_connect():
    if 'user_id' not in session:
        return False
    emit('message', {'data': f'Bienvenido al chat!. Como puedo ayudarte hoy?'})

@socketio.on('message')
def handle_message(data):
    if 'user_id' not in session:
        emit('message', {'data': 'Please log in to use the chat.'})
        return

    user_message = data.get('message', '').lower()
    print(user_message)
    # Manejar las sugerencias específicas
    # if "how do i make a booking" in user_message:
    if "¿cómo hago una reserva" in user_message:
        response = """
Para realizar una reserva, sigue estos pasos:
1. Haz clic en el botón "Nueva reserva" en la parte superior del panel de control
2. Selecciona el campo deportivo que prefieras
3. Elige la fecha y la hora
4. Revisa el precio total
5. Confirma tu reserva
¿Quieres que te muestre ahora los campos disponibles?
"""
        emit('message', {'data': response})

    elif "¿cuáles son sus precios" in user_message:
        fields = get_field_prices()
        response = "Aquí están nuestros precios actuales.:\n"
        for field in fields:
            response += f"• {field['name']}: S/{field['price_per_hour']} por hora\n"
        response += "\nLos precios pueden variar dependiendo de las horas pico y eventos especiales.."
        emit('message', {'data': response})

    elif "¿cómo puedo cancelar mi reserva" in user_message:
        bookings = get_user_bookings(session['user_id'])
        pending_bookings = [b for b in bookings if b['status'] == 'pending']

        if pending_bookings:
            response = "Tienes las siguientes reservas pendientes que se pueden cancelar:\n"
            for booking in pending_bookings:
                response += f"• {booking['field_name']} on {booking['booking_date'].strftime('%Y-%m-%d')} "
                response += f"at {booking['start_time']} - {booking['end_time']}\n"
            response += "\nPara cancelar, haga clic en el botón 'Cancelar' junto a la reserva que desea cancelar.."
        else:
            response = "No tienes ninguna reserva pendiente que se pueda cancelar."
        emit('message', {'data': response})

    elif "¿cúal es su horario de atención" in user_message:
        response = """
Nuestras instalaciones están abiertas:
• Lunes a viernes: 8:00 a 22:00 horas
• Sábados y domingos: 9:00 a 20:00 horas

Los horarios en días festivos pueden variar. ¿Quieres consultar disponibilidad para una fecha concreta?
"""
        emit('message', {'data': response})

    elif "¿cómo puedo contactar con el servicio al cliente" in user_message:
        response = """
Puede comunicarse con nuestro equipo de soporte a través de:
• Correo electrónico: support@sportsbooking.com
• Teléfono: 123-456-7890
• WhatsApp: +1 234-567-8900
• Visite nuestra oficina: de lunes a viernes, de 9:00 a 17:00

Nuestro tiempo de respuesta promedio es de menos de 2 horas durante el horario comercial.
"""
        emit('message', {'data': response})

    # Manejar palabras clave adicionales
    elif any(word in user_message for word in ['hola', 'hi', 'hey', 'hello']):
        response = f"Hola {session.get('username')}! ¿Cómo puedo ayudarle hoy?"
        emit('message', {'data': response})

    elif 'precio' in user_message:
        fields = get_field_prices()
        response = "Aquí están nuestros precios actuales.:\n\n"
        for field in fields:
            response += f"• {field['name']}: S/{field['price_per_hour']} por hora\n"
        emit('message', {'data': response})

    elif 'disponibilidad' in user_message:
        response = "¿Quieres consultar la disponibilidad para una fecha concreta? Utiliza el formulario de reservas para ver los horarios disponibles."
        emit('message', {'data': response})

    elif 'pago' in user_message:
        response = """
Aceptamos los siguientes métodos de pago:
• Tarjetas de crédito/débito
• PayPal
• Transferencia bancaria
• Efectivo (en nuestra oficina)

El pago se debe realizar al momento de la reserva.
"""
        emit('message', {'data': response})

    else:
        response = """
No estoy seguro de cómo ayudarte con eso. Aquí hay algunas cosas con las que puedo ayudarte:
• Hacer una reserva
• Consultar precios
• Cancelar reservas
• Horario de atención
• Información de contacto

Selecciona uno de estos temas o reformula tu pregunta.
"""
        emit('message', {'data': response})
def get_user_bookings(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT b.*, f.name as field_name
        FROM bookings b
        JOIN fields f ON b.field_id = f.id
        WHERE b.user_id = %s
    ''', (user_id,))
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()
    return bookings

def get_field_prices():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT name, price_per_hour FROM fields')
    fields = cursor.fetchall()
    cursor.close()
    conn.close()
    return fields

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',port=5000,debug=True)