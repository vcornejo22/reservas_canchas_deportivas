from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
import os 
from datasets import Dataset
import gradio as gr

# Cargar el modelo y el tokenizador
model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"  
# path_data = os.getcwd() + "/data/train.json"
messages = {
    "messages": [
      {
        "role": "user",
        "content": "¿Cómo reservo un campo de fútbol?"
      },
      {
        "role": "assistant",
        "content": "Puedes reservar un campo de fútbol desde nuestra web. Solo tienes que seleccionar la fecha, hora y campo disponible, y completar el pago."
      },
      {
        "role": "user",
        "content": "¿Cuánto cuesta reservar un campo de tenis?"
      },
      {
        "role": "assistant",
        "content": "No contamos con un campo de tenis por el momento."
      }, 
      {
        "role": "user",
        "content": "¿Qué horarios tienen disponibles para reservar una cancha de fútbol?"
    },
    {
        "role": "assistant",
        "content": "Nuestros campos de fútbol están disponibles de lunes a domingo, desde las 8:00 AM hasta las 10:00 PM. Puedes verificar la disponibilidad específica para cada horario en nuestra plataforma de reservas."
    },
    {
        "role": "user",
        "content": "¿Tienen canchas de básquet?"
    },
    {
        "role": "assistant",
        "content": "Por el momento solo contamos con campos de fútbol disponibles para reserva. Estamos trabajando en expandir nuestras instalaciones en el futuro."
    },
    {
        "role": "user",
        "content": "¿Cuál es el precio por hora?"
    },
    {
        "role": "assistant",
        "content": "El precio por hora del campo de fútbol es de S/50. Ofrecemos descuentos especiales para reservas de más de 2 horas y para clientes frecuentes."
    },{
        "role": "user",
        "content": "¿Puedo cancelar una reserva?"
    },
    {
        "role": "assistant",
        "content": "Sí, puedes cancelar tu reserva hasta 24 horas antes de la hora programada para recibir un reembolso completo. Las cancelaciones con menos de 24 horas de anticipación tienen un cargo del 50%."
    },
    {
        "role": "user",
        "content": "¿Tienen iluminación nocturna?"
    },
    {
        "role": "assistant",
        "content": "Sí, todos nuestros campos de fútbol cuentan con iluminación profesional para partidos nocturnos, permitiendo jugar cómodamente hasta las 10:00 PM."
    },{
        "role": "user",
        "content": "¿Cómo puedo reservar un campo de fútbol?"
      },
      {
        "role": "assistant",
        "content": "Puedes reservar un campo de fútbol ingresando a nuestro sitio web, seleccionando la fecha, hora y campo que desees, y luego confirmando tu reserva con el pago."
      },
      {
        "role": "user",
        "content": "¿Tienen campos para otros deportes?"
      },
      {
        "role": "assistant",
        "content": "Por el momento, solo contamos con campos para fútbol. Estamos trabajando para agregar más opciones en el futuro."
      },
      {
        "role": "user",
        "content": "¿Qué horarios están disponibles para reservar?"
      },
      {
        "role": "assistant",
        "content": "Nuestros campos están disponibles para reserva de lunes a domingo, desde las 8:00 a.m. hasta las 10:00 p.m. La disponibilidad específica depende de las reservas ya realizadas."
      },
      {
        "role": "user",
        "content": "¿Cómo puedo cancelar una reserva?"
      },
      {
        "role": "assistant",
        "content": "Para cancelar una reserva, ingresa a tu cuenta en nuestro sitio web, ve a la sección 'Mis Reservas', selecciona la reserva que deseas cancelar y haz clic en 'Cancelar'. Recuerda revisar nuestras políticas de cancelación."
      },
      {
        "role": "user",
        "content": "¿Qué métodos de pago aceptan?"
      },
      {
        "role": "assistant",
        "content": "Aceptamos pagos con tarjeta de crédito, débito y transferencias bancarias. Pronto agregaremos más métodos de pago."
      },
      {
        "role": "user",
        "content": "¿Puedo hacer una reserva por teléfono?"
      },
      {
        "role": "assistant",
        "content": "Por ahora, todas las reservas deben realizarse a través de nuestra plataforma web para garantizar disponibilidad y rapidez en el proceso."
      },
      {
        "role": "user",
        "content": "¿Qué pasa si llego tarde a mi reserva?"
      },
      {
        "role": "assistant",
        "content": "Si llegas tarde a tu reserva, el tiempo perdido no será reembolsado. Te recomendamos llegar 10 minutos antes para aprovechar al máximo tu tiempo en el campo."
      },
      {
        "role": "user",
        "content": "¿Puedo modificar la hora de mi reserva?"
      },
      {
        "role": "assistant",
        "content": "Sí, puedes modificar la hora de tu reserva siempre y cuando haya disponibilidad. Ve a la sección 'Mis Reservas' en nuestra web y selecciona la opción de modificar."
      },
      {
        "role": "user",
        "content": "¿Qué sucede si llueve durante mi reserva?"
      },
      {
        "role": "assistant",
        "content": "En caso de lluvia, te ofreceremos la posibilidad de reprogramar tu reserva para otra fecha. Contáctanos a través del soporte para gestionar este cambio."
      },
      {
        "role": "user",
        "content": "¿Ofrecen descuentos para reservas frecuentes?"
      },
      {
        "role": "assistant",
        "content": "¡Sí! Contamos con descuentos para clientes frecuentes. Si reservas más de tres veces al mes, recibirás un descuento en tu próxima reserva."
      },
      {
        "role": "user",
        "content": "¿Puedo reservar varias horas seguidas?"
      },
      {
        "role": "assistant",
        "content": "Sí, puedes reservar varias horas seguidas, siempre que el horario esté disponible. Selecciona las horas consecutivas al realizar tu reserva en nuestra plataforma."
      },
      {
        "role": "user",
        "content": "¿Qué medidas de seguridad tienen en los campos?"
      },
      {
        "role": "assistant",
        "content": "Contamos con personal capacitado, cámaras de seguridad y una política de primeros auxilios en caso de emergencias para garantizar tu seguridad mientras disfrutas del juego."
      },
      {
        "role": "user",
        "content": "¿Hay estacionamiento cerca de los campos?"
      },
      {
        "role": "assistant",
        "content": "Sí, contamos con un estacionamiento gratuito cercano a los campos para nuestros clientes."
      },
      {
        "role": "user",
        "content": "¿Ofrecen alquiler de balones o equipo deportivo?"
      },
      {
        "role": "assistant",
        "content": "Sí, puedes alquilar balones de fútbol y otros accesorios directamente en el lugar. Consulta nuestra sección de servicios adicionales al momento de reservar."
      },
      {
        "role": "user",
        "content": "¿Cuáles son las dimensiones de los campos?"
      },
      {
        "role": "assistant",
        "content": "Nuestros campos tienen dimensiones estándar para fútbol 7: 50 metros de largo por 30 metros de ancho. Si necesitas más información, no dudes en preguntar."
      },
      {
        "role": "user",
        "content": "¿Puedo traer comida o bebidas al campo?"
      },
      {
        "role": "assistant",
        "content": "Está permitido traer bebidas, pero por razones de seguridad no se permite el ingreso de comida al área del campo. Contamos con un snack bar cercano donde puedes adquirir alimentos."
      }, 
      {
        "role": "user",
        "content": "¿Tienen vestidores?"
    },
    {
        "role": "assistant",
        "content": "Sí, contamos con vestidores completos para hombres y mujeres, equipados con duchas, casilleros y baños."
    },
    {
        "role": "user",
        "content": "¿Hay estacionamiento?"
    },
    {
        "role": "assistant",
        "content": "Sí, disponemos de estacionamiento gratuito para nuestros clientes con capacidad para 30 vehículos."
    },
    {
        "role": "user",
        "content": "¿Tienen servicio de alquiler de balones?"
    },
    {
        "role": "assistant",
        "content": "Sí, ofrecemos servicio de alquiler de balones por S/5 por partido. También puedes traer tu propio balón si lo prefieres."
    },
    {
        "role": "user",
        "content": "¿El campo es techado?"
    },
    {
        "role": "assistant",
        "content": "No, nuestros campos son al aire libre, pero contamos con un buen sistema de drenaje para días lluviosos."
    },
    {
        "role": "user",
        "content": "¿Tienen cafetería o venta de bebidas?"
    },
    {
        "role": "assistant",
        "content": "Sí, contamos con una cafetería que ofrece bebidas hidratantes, agua, snacks y comida rápida. También tenemos máquinas expendedoras cerca de los campos."
    },
    {
        "role": "user",
        "content": "¿Qué tipo de superficie tiene la cancha?"
    },
    {
        "role": "assistant",
        "content": "Nuestros campos son de césped sintético de última generación, con un mantenimiento regular para garantizar su óptimo estado."
    },
    {
        "role": "user",
        "content": "¿Tienen área para espectadores?"
    },
    {
        "role": "assistant",
        "content": "Sí, cada campo cuenta con graderías techadas con capacidad para 50 personas, donde los espectadores pueden ver cómodamente los partidos."
    },
    {
        "role": "user",
        "content": "¿Tienen wifi?"
    },
    {
        "role": "assistant",
        "content": "Sí, ofrecemos wifi gratuito en todas nuestras instalaciones. La contraseña se proporciona en recepción al momento de tu llegada."
    },
    {
        "role": "user",
        "content": "¿Tienen botiquín de primeros auxilios?"
    },
    {
        "role": "assistant",
        "content": "Sí, contamos con botiquín de primeros auxilios y personal capacitado para emergencias básicas. También tenemos convenio con servicios de emergencia cercanos."
    },
    {
        "role": "user",
        "content": "¿Puedo pagar en efectivo al llegar?"
      },
      {
        "role": "assistant",
        "content": "Por el momento, todas las reservas deben pagarse en línea a través de nuestra plataforma para confirmar la disponibilidad."
      },
      {
        "role": "user",
        "content": "¿Qué pasa si otra persona está usando el campo que reservé?"
      },
      {
        "role": "assistant",
        "content": "Si esto ocurre, contacta a nuestro personal de soporte inmediatamente. Nos aseguraremos de resolver el problema y garantizar tu tiempo reservado."
      },
      {
        "role": "user",
        "content": "¿Tienen algún código de vestimenta para usar los campos?"
      },
      {
        "role": "assistant",
        "content": "Recomendamos el uso de ropa deportiva y zapatillas adecuadas para césped sintético. El uso de tacos metálicos no está permitido para preservar la calidad del campo."
      },
      {
        "role": "user",
        "content": "¿Hay vestuarios en las instalaciones?"
      },
      {
        "role": "assistant",
        "content": "Sí, nuestras instalaciones cuentan con vestuarios equipados con duchas y casilleros para tu comodidad."
      },
      {
        "role": "user",
        "content": "¿Puedo reservar un campo para un torneo?"
      },
      {
        "role": "assistant",
        "content": "¡Claro! Para reservar un campo para un torneo, contáctanos directamente para coordinar los detalles y asegurarte de que todo esté listo para el evento."
      },
      {
        "role": "user",
        "content": "¿Qué hago si mi reserva no aparece en mi cuenta?"
      },
      {
        "role": "assistant",
        "content": "Si tu reserva no aparece en tu cuenta, verifica que el pago se haya procesado correctamente. Si el problema persiste, contáctanos a través del soporte con los detalles de tu reserva."
      },
      {
        "role": "user",
        "content": "¿Los campos están disponibles los días feriados?"
      },
      {
        "role": "assistant",
        "content": "Sí, los campos están disponibles los días feriados. Sin embargo, te recomendamos reservar con anticipación, ya que suelen ser días de alta demanda."
      },
      {
        "role": "user",
        "content": "¿Ofrecen reembolsos por cancelaciones?"
      },
      {
        "role": "assistant",
        "content": "Sí, ofrecemos reembolsos si la cancelación se realiza con al menos 24 horas de anticipación. Consulta nuestras políticas de cancelación para más detalles."
      },
      {
        "role": "user",
        "content": "¿Cuánto tiempo dura una reserva de campo?"
      },
      {
        "role": "assistant",
        "content": "Cada reserva tiene una duración de 1 hora. Si deseas más tiempo, puedes agregar horas adicionales durante el proceso de reserva."
      },
      {
        "role": "user",
        "content": "¿Puedo reservar para una liga semanal?"
      },
      {
        "role": "assistant",
        "content": "Sí, ofrecemos planes para ligas semanales. Contáctanos para coordinar las fechas y horarios fijos."
      },
      {
        "role": "user",
        "content": "¿Qué pasa si se va la luz durante mi reserva?"
      },
      {
        "role": "assistant",
        "content": "En caso de un corte de luz, reprogramaremos tu reserva sin costo adicional. Nos disculpamos por cualquier inconveniente."
      },
      {
        "role": "user",
        "content": "¿Hay áreas de espera para los jugadores?"
      },
      {
        "role": "assistant",
        "content": "Sí, contamos con áreas de espera cerca de los campos, donde los jugadores pueden descansar antes o después de su reserva."
      },
      {
        "role": "user",
        "content": "¿Puedo llevar a mi mascota mientras juego?"
      },
      {
        "role": "assistant",
          "content": "Lamentablemente, no está permitido llevar mascotas a las áreas de juego por razones de seguridad y limpieza."
      },
      {
        "role": "user",
        "content": "¿Hay un límite de jugadores por campo?"
      },
      {
        "role": "assistant",
        "content": "Recomendamos un máximo de 14 jugadores por campo para garantizar un juego cómodo y seguro."
      },
      {
        "role": "user",
        "content": "¿Tienen promociones para grupos?"
    },
    {
        "role": "assistant",
        "content": "Sí, ofrecemos un 15% de descuento para reservas regulares semanales y un 20% para escuelas de fútbol o equipos que reserven más de 4 horas semanales."
    },
    {
        "role": "user",
        "content": "¿Qué hago si hay algún problema con las instalaciones durante mi reserva?"
    },
    {
        "role": "assistant",
        "content": "Contamos con personal de mantenimiento disponible durante todo el horario de operación. Puedes reportar cualquier inconveniente en recepción o llamar al número de emergencias interno: (+1) 999-8888."
    },
    {
        "role": "user",
        "content": "¿Organizan torneos?"
    },
    {
        "role": "assistant",
        "content": "Sí, organizamos torneos mensuales para diferentes categorías. Puedes inscribir a tu equipo en recepción o través de nuestra web. Ofrecemos premios y trofeos para los ganadores."
    },
    {
        "role": "user",
        "content": "¿Tienen servicio de árbitros?"
    },
    {
        "role": "assistant",
        "content": "Sí, contamos con árbitros certificados disponibles por un costo adicional de S/30 por partido. Debes solicitar este servicio con al menos 24 horas de anticipación."
    },
    {
        "role": "user",
        "content": "¿Qué pasa si llueve el día de mi reserva?"
    },
    {
        "role": "assistant",
        "content": "En caso de lluvia fuerte que impida el juego, te ofrecemos la opción de reprogramar tu reserva sin costo adicional o recibir un reembolso completo."
    },
    {
        "role": "user",
        "content": "¿Puedo modificar mi reserva?"
    },
    {
        "role": "assistant",
        "content": "Sí, puedes modificar tu reserva hasta 48 horas antes sin costo. Cambios con menos tiempo tienen un cargo administrativo de S/10, sujeto a disponibilidad."
    },
    {
        "role": "user",
        "content": "¿Tienen servicio de entrenador personal?"
    },
    {
        "role": "assistant",
        "content": "Sí, contamos con entrenadores certificados disponibles para clases particulares o grupales. Las tarifas comienzan en S/40 por hora. Puedes consultar sus perfiles y disponibilidad en nuestra web."
    },
    {
        "role": "user",
        "content": "¿Cómo puedo presentar una queja o sugerencia?"
    },
    {
        "role": "assistant",
        "content": "Puedes presentar quejas o sugerencias a través de nuestro formulario en línea, en el libro de reclamaciones en recepción, o enviando un email a atencion@canchas.com. Respondemos en un máximo de 24 horas."
    },
    {
        "role": "user",
        "content": "¿Cómo puedo reservar un campo?"
      },
      {
        "role": "assistant",
        "content": "¡Súper fácil! Solo entra a nuestra página, elige el día y la hora que te convenga, y confirma la reserva. ¡No olvides completar el pago para asegurar tu lugar!"
      },
      {
        "role": "user",
        "content": "¿Qué pasa si llego tarde?"
      },
      {
        "role": "assistant",
        "content": "Tranquilo, el campo estará listo para ti, pero el tiempo perdido no se recupera. ¡Así que trata de llegar un poquito antes para aprovechar al máximo!"
      },
      {
        "role": "user",
        "content": "¿Hay algo más aparte de fútbol?"
      },
      {
        "role": "assistant",
        "content": "Por ahora, solo fútbol, pero estamos trabajando en traer más deportes pronto. ¡Mantente atento!"
      },
      {
        "role": "user",
        "content": "¿Qué hago si no puedo ir el día que reservé?"
      },
      {
        "role": "assistant",
        "content": "No pasa nada, puedes cambiar la fecha desde tu cuenta en nuestra web, siempre y cuando lo hagas con tiempo. 😉"
      },
      {
        "role": "user",
        "content": "¿Puedo llevar comida al campo?"
      },
      {
        "role": "assistant",
        "content": "¡Claro! Solo asegúrate de mantener el área limpia. Y si no quieres llevar nada, tenemos un snack bar con todo lo necesario. 🍔⚽"
      },
      {
        "role": "user",
        "content": "¿Hay descuentos?"
      },
      {
        "role": "assistant",
        "content": "¡Obvio! Si reservas varias veces al mes, te damos un descuentazo. ¡Es nuestra manera de agradecerte!"
      },
      {
        "role": "user",
        "content": "¿Qué pasa si hay mal clima?"
      },
      {
        "role": "assistant",
        "content": "Si el clima no coopera, no te preocupes. Te ayudamos a reprogramar tu reserva sin costo adicional. 😊"
      },        {
        "role": "user",
        "content": "¿Cómo puedo reservar un campo de fútbol?"
    },
    {
        "role": "assistant",
        "content": "¡Súper fácil! Solo entra a nuestra página, elige el día y la hora que te convenga, y confirma la reserva. ¡No olvides completar el pago para asegurar tu lugar!"
    },
    {
        "role": "user",
        "content": "¿Qué pasa si llego tarde?"
    },
    {
        "role": "assistant",
        "content": "Tranquilo, el campo estará listo para ti, pero el tiempo perdido no se recupera. ¡Así que trata de llegar un poquito antes para aprovechar al máximo!"
    },
    {
        "role": "user",
        "content": "¿Hay algo más aparte de fútbol?"
    },
    {
        "role": "assistant",
        "content": "Por ahora, solo fútbol, pero estamos trabajando en traer más deportes pronto. ¡Mantente atento!"
    },
    {
        "role": "user",
        "content": "¿Qué hago si no puedo ir el día que reservé?"
    },
    {
        "role": "assistant",
        "content": "No pasa nada, puedes cambiar la fecha desde tu cuenta en nuestra web, siempre y cuando lo hagas con tiempo. 😉"
    },
    {
        "role": "user",
        "content": "¿Puedo llevar comida al campo?"
    },
    {
        "role": "assistant",
        "content": "¡Claro! Solo asegúrate de mantener el área limpia. Y si no quieres llevar nada, tenemos un snack bar con todo lo necesario. 🍔⚽"
    },
    {
        "role": "user",
        "content": "¿Hay descuentos?"
    },
    {
        "role": "assistant",
        "content": "¡Obvio! Si reservas varias veces al mes, te damos un descuentazo. ¡Es nuestra manera de agradecerte!"
    },
    {
        "role": "user",
        "content": "¿Qué pasa si hay mal clima?"
    },
    {
        "role": "assistant",
        "content": "Si el clima no coopera, no te preocupes. Te ayudamos a reprogramar tu reserva sin costo adicional. 😊"
    },
    {
        "role": "user",
        "content": "¿Hay algún servicio de limpieza?"
    },
    {
        "role": "assistant",
        "content": "¡Claro! Nuestro equipo de limpieza se encargará de mantener tu campo limpio y listo para el próximo partido. ¡No te preocupes!"
    },
    {
        "role": "user",
        "content": "¿Hay algún servicio de mantenimiento?"
    },
    {
        "role": "assistant",
        "content": "¡Claro! Nuestro equipo de mantenimiento se encargará de mantener tu campo en perfecto estado. ¡No te preocupes!"
    },
    {
        "role": "user",
        "content": "¿Hay algún servicio de seguridad?"
    },
    {
        "role": "assistant",
        "content": "¡Claro! Nuestro equipo de seguridad se encargará de mantener tu campo seguro. ¡No te preocupes!"
    },
    {
        "role": "user",
        "content": "¿Hay algún servicio de transporte?"
    },
    {
        "role": "assistant",
        "content": "¡No! Por el momento no contamos con ese servicio."
    }, 
    {
        "role": "user",
        "content": "¿Tienen pelotas profesionales?"
    },
    {
        "role": "assistant",
        "content": "¡Sí! Tenemos balones oficiales Nike y Adidas para alquilar por S/5. ¡Están en perfectas condiciones! 🏆⚽"
    },
    {
        "role": "user",
        "content": "¿Se puede reservar para un cumpleaños?"
    },
    {
        "role": "assistant",
        "content": "¡Por supuesto! 🎉 Tenemos paquetes especiales para cumpleaños que incluyen 2 horas de campo, área para torta y decoración básica. ¡Escríbenos para más detalles!"
    },
    {
        "role": "user",
        "content": "¿Tienen promociones para estudiantes?"
    },
    {
        "role": "assistant",
        "content": "¡Claro que sí! 📚 Con tu carnet de estudiante tienes 15% de descuento de lunes a viernes hasta las 5pm. ¡Aprovecha!"
    },
    {
        "role": "user",
        "content": "¿Qué pasa si me lesiono jugando?"
    },
    {
        "role": "assistant",
        "content": "¡Tu seguridad es primero! 🏥 Tenemos botiquín de primeros auxilios y personal capacitado. Además, estamos cerca de una clínica por si necesitas atención adicional."
    },
    {
        "role": "user",
        "content": "¿Puedo hacer una reserva recurrente?"
    },
    {
        "role": "assistant",
        "content": "¡Claro! 📅 Puedes programar reservas semanales y te damos 20% de descuento. ¡Perfecto para equipos que entrenan regularmente!"
    },
    {
        "role": "user",
        "content": "¿Tienen servicio de fotos o video?"
    },
    {
        "role": "assistant",
        "content": "¡Sí! 📸 Podemos grabar tu partido por S/30 la hora. ¡Perfecto para analizar jugadas o guardar momentos especiales!"
    },
    {
        "role": "user",
        "content": "¿Hay wifi en las canchas?"
    },
    {
        "role": "assistant",
        "content": "¡Por supuesto! 📱 Tenemos wifi gratis en toda la instalación. La clave te la damos cuando llegues. ¡Comparte tus mejores jugadas!"
    },
    {
        "role": "user",
        "content": "¿Tienen alguna app móvil?"
    },
    {
        "role": "assistant",
        "content": "¡Sí! 📱 Descarga nuestra app para reservar más fácil, ver disponibilidad en tiempo real y acceder a promociones exclusivas. ¡Búscanos como 'CanchasApp'!"
    },
    {
        "role": "user",
        "content": "¿Qué medidas de bioseguridad tienen?"
    },
    {
        "role": "assistant",
        "content": "¡Tu salud es prioridad! 😷 Desinfectamos los campos entre partidos, tenemos dispensadores de gel y control de aforo. ¡Juega tranquilo!"
    },
    {
        "role": "user",
        "content": "¿Tienen servicio de hidratación?"
    },
    {
        "role": "assistant",
        "content": "¡Claro! 🥤 Tenemos máquinas expendedoras con bebidas deportivas, agua y snacks. También puedes traer tus propias bebidas."
    },
    {
        "role": "user",
        "content": "¿Se puede hacer una reserva para ver un partido importante?"
    },
    {
        "role": "assistant",
        "content": "¡Sí! 📺 Tenemos área con pantalla gigante para ver partidos. Reserva con anticipación para eventos importantes. ¡Trae a tus amigos!"
    },
    {
        "role": "user",
        "content": "¿Tienen algún grupo de WhatsApp para reservas?"
    },
    {
        "role": "assistant",
        "content": "¡Todo es por la web! 💻 Así aseguramos que las reservas se manejen en orden y tengas tu confirmación al instante. ¡Es más seguro!"
    },
    {
        "role": "user",
        "content": "¿Puedo organizar un campeonato?"
    },
    {
        "role": "assistant",
        "content": "¡Claro que sí! 🏆 Tenemos paquetes especiales para torneos, incluyen arbitraje, premios y organización. ¡Contáctanos para más detalles!"
    },
    {
        "role": "user",
        "content": "¿Tienen servicio de uniformes?"
    },
    {
        "role": "assistant",
        "content": "¡Sí! 👕 Alquilamos chalecos de diferentes colores por S/2 por unidad. ¡Perfectos para distinguir los equipos!"
    }
    ]
}

dataset = Dataset.from_dict({
    "messages": messages['messages']
})

tokenizer = AutoTokenizer.from_pretrained(model_name)

def preprocess(examples):
    conversations = []
    for message in examples:
        if message["role"] == "user":
            conversations.append("User: " + message["content"])
        elif message["role"] == "assistant":
            conversations.append("Assistant: " + message["content"])
    return tokenizer('\n'.join(conversations), truncation=True, padding=True)

data_tokens = {
    "input_ids": [],
    "attention_mask": []
}

for message in messages['messages']:
    tokens = preprocess([message])
    data_tokens["input_ids"].extend(tokens["input_ids"])
    data_tokens["attention_mask"].extend(tokens["attention_mask"])


model = AutoModelForCausalLM.from_pretrained(model_name)

training_args = TrainingArguments(
    output_dir="./chatbot",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    num_train_epochs=3,
    save_total_limit=2,
    logging_dir="./logs",
)

trainer = Trainer(
    model=model,
    args = training_args,
    train_dataset= dataset
)

trainer.train()

model.save_pretrained("./chatbot")
tokenizer.save_pretrained("./chatbot")

# Para probarlo
def chat(input_text):
    inputs = tokenizer(f"User: {input_text}\nAssistant:", return_tensors="pt")
    outputs = model.generate(**inputs, max_length=50)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

gr.Interface(fn=chat, inputs="text", outputs="text", title="Chatbot Deportivo").launch()
