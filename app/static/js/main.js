// Función para validar el formulario de registro
function validateRegistrationForm() {
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');

    if (password.value !== confirmPassword.value) {
        alert('Passwords do not match!');
        return false;
    }
    return true;
}

// Función para validar el formulario de reserva
function validateBookingForm() {
    const startTime = document.getElementById('start_time').value;
    const endTime = document.getElementById('end_time').value;

    if (startTime >= endTime) {
        alert('End time must be after start time!');
        return false;
    }
    return true;
}

// Inicializar elementos cuando el DOM esté cargado
document.addEventListener('DOMContentLoaded', function() {
    // Establecer la fecha mínima para las reservas como hoy
    const bookingDate = document.getElementById('booking_date');
    if (bookingDate) {
        const today = new Date().toISOString().split('T')[0];
        bookingDate.min = today;
    }

    // Agregar validaciones a los formularios
    const registerForm = document.querySelector('form[action="/register"]');
    if (registerForm) {
        registerForm.onsubmit = validateRegistrationForm;
    }

    const bookingForm = document.querySelector('form[action="/booking"]');
    if (bookingForm) {
        bookingForm.onsubmit = validateBookingForm;
    }
});