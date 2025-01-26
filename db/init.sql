CREATE DATABASE IF NOT EXISTS sports_booking;
USE sports_booking;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fields (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price_per_hour DECIMAL(10,2) NOT NULL
);


CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    field_id INT,
    booking_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'confirmed', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (field_id) REFERENCES fields(id)
);


-- Limpiar datos existentes (si es necesario)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE bookings;
TRUNCATE TABLE users;
TRUNCATE TABLE fields;
SET FOREIGN_KEY_CHECKS = 1;

-- Insertar usuarios ficticios
INSERT INTO users (username, password, email, created_at, phone) VALUES
-- La contraseña hasheada corresponde a 'password123' para todos los usuarios
('juan', 'scrypt:32768:8:1$XyBigg62YaA9tuKL$b4e43b0ad88a15e4a9786290520aefac893dc3e561bc99895330b02daa3e2931c9fb88efda986eba39bbdbcf4c06bf595de4e42b71498240e2169dca2b62474e', 'juan.perez@email.com', '2024-01-10 08:30:00', '999999999'),
('maria', 'scrypt:32768:8:1$XyBigg62YaA9tuKL$b4e43b0ad88a15e4a9786290520aefac893dc3e561bc99895330b02daa3e2931c9fb88efda986eba39bbdbcf4c06bf595de4e42b71498240e2169dca2b62474e', 'maria.garcia@email.com', '2024-01-11 09:15:00', '999999999'),
('carlos', 'scrypt:32768:8:1$XyBigg62YaA9tuKL$b4e43b0ad88a15e4a9786290520aefac893dc3e561bc99895330b02daa3e2931c9fb88efda986eba39bbdbcf4c06bf595de4e42b71498240e2169dca2b62474e', 'carlos.rodriguez@email.com', '2024-01-12 10:45:00', '999999999'),
('ana', 'scrypt:32768:8:1$XyBigg62YaA9tuKL$b4e43b0ad88a15e4a9786290520aefac893dc3e561bc99895330b02daa3e2931c9fb88efda986eba39bbdbcf4c06bf595de4e42b71498240e2169dca2b62474e', 'ana.martinez@email.com', '2024-01-13 14:20:00', '999999999'),
('pedro', 'scrypt:32768:8:1$XyBigg62YaA9tuKL$b4e43b0ad88a15e4a9786290520aefac893dc3e561bc99895330b02daa3e2931c9fb88efda986eba39bbdbcf4c06bf595de4e42b71498240e2169dca2b62474e', 'pedro.sanchez@email.com', '2024-01-14 16:00:00', '999999999');

-- Insertar campos deportivos
INSERT INTO fields (name, description, price_per_hour) VALUES
('Cancha Sintética A', 'Cancha de fútbol 7 con césped sintético de última generación. Incluye iluminación LED y redes de alta calidad.', 50.00),
('Cancha Sintética B', 'Cancha de fútbol 5 ideal para partidos rápidos. Césped sintético profesional y arcos reglamentarios.', 40.00),
('Cancha Premium', 'Cancha de fútbol 11 con césped sintético profesional, vestuarios y área de calentamiento.', 80.00),
('Cancha Indoor', 'Cancha techada con césped sintético, perfecta para jugar en cualquier clima. Incluye sistema de ventilación.', 60.00),
('Cancha Multideporte', 'Cancha versátil adaptable para fútbol 5 o básquet. Superficie sintética multiuso.', 45.00);

-- Insertar reservas ficticias
INSERT INTO bookings (user_id, field_id, booking_date, start_time, end_time, total_price, status, created_at) VALUES
-- Reservas para Juan Pérez
(1, 1, '2024-01-25', '15:00:00', '16:00:00', 50.00, 'confirmed', '2024-01-20 09:00:00'),
(1, 2, '2024-01-26', '18:00:00', '19:00:00', 40.00, 'pending', '2024-01-20 10:30:00'),

-- Reservas para María García
(2, 3, '2024-01-25', '16:00:00', '18:00:00', 160.00, 'confirmed', '2024-01-19 14:00:00'),
(2, 1, '2024-01-27', '14:00:00', '15:00:00', 50.00, 'cancelled', '2024-01-19 15:30:00'),

-- Reservas para Carlos Rodríguez
(3, 4, '2024-01-26', '19:00:00', '21:00:00', 120.00, 'confirmed', '2024-01-20 11:15:00'),
(3, 2, '2024-01-28', '17:00:00', '18:00:00', 40.00, 'pending', '2024-01-20 12:00:00'),

-- Reservas para Ana Martínez
(4, 5, '2024-01-27', '16:00:00', '17:00:00', 45.00, 'confirmed', '2024-01-21 09:45:00'),
(4, 3, '2024-01-29', '15:00:00', '17:00:00', 160.00, 'pending', '2024-01-21 10:30:00'),

-- Reservas para Pedro Sánchez
(5, 1, '2024-01-28', '20:00:00', '22:00:00', 100.00, 'confirmed', '2024-01-22 16:00:00'),
(5, 4, '2024-01-30', '18:00:00', '19:00:00', 60.00, 'pending', '2024-01-22 17:30:00');

-- Insertar más reservas para fechas futuras
INSERT INTO bookings (user_id, field_id, booking_date, start_time, end_time, total_price, status, created_at) VALUES
(1, 3, '2024-02-01', '17:00:00', '19:00:00', 160.00, 'confirmed', '2024-01-23 09:00:00'),
(2, 4, '2024-02-02', '16:00:00', '17:00:00', 60.00, 'pending', '2024-01-23 10:00:00'),
(3, 5, '2024-02-03', '18:00:00', '20:00:00', 90.00, 'confirmed', '2024-01-23 11:00:00'),
(4, 1, '2024-02-04', '15:00:00', '16:00:00', 50.00, 'pending', '2024-01-23 12:00:00'),
(5, 2, '2024-02-05', '19:00:00', '21:00:00', 80.00, 'confirmed', '2024-01-23 13:00:00');

-- Insertar algunas estadísticas de uso para las canchas
INSERT INTO bookings (user_id, field_id, booking_date, start_time, end_time, total_price, status, created_at) VALUES
-- Reservas pasadas
(1, 1, '2024-01-15', '14:00:00', '15:00:00', 50.00, 'confirmed', '2024-01-10 09:00:00'),
(2, 1, '2024-01-16', '16:00:00', '17:00:00', 50.00, 'confirmed', '2024-01-10 10:00:00'),
(3, 2, '2024-01-17', '15:00:00', '16:00:00', 40.00, 'confirmed', '2024-01-10 11:00:00'),
(4, 3, '2024-01-18', '18:00:00', '20:00:00', 160.00, 'confirmed', '2024-01-10 12:00:00'),
(5, 4, '2024-01-19', '17:00:00', '18:00:00', 60.00, 'confirmed', '2024-01-10 13:00:00');

-- Insertar algunas reservas canceladas
INSERT INTO bookings (user_id, field_id, booking_date, start_time, end_time, total_price, status, created_at) VALUES
(1, 5, '2024-01-20', '15:00:00', '16:00:00', 45.00, 'cancelled', '2024-01-15 09:00:00'),
(2, 4, '2024-01-21', '16:00:00', '17:00:00', 60.00, 'cancelled', '2024-01-15 10:00:00'),
(3, 3, '2024-01-22', '17:00:00', '18:00:00', 80.00, 'cancelled', '2024-01-15 11:00:00');
