-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS gym_management;
USE gym_management;

-- Tabla de socios
CREATE TABLE socios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(15),
    direccion VARCHAR(255),
    password VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    estado ENUM('activo', 'vencida', 'gracia') DEFAULT 'vencida'
);

-- Tabla de cuotas
CREATE TABLE cuotas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    socio_id INT NOT NULL,
    fecha_pago DATE NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    estado ENUM('activa', 'vencida', 'gracia') DEFAULT 'vencida',
    monto DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (socio_id) REFERENCES socios(id)
);

-- Tabla de actividades
CREATE TABLE actividades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    dias_habilitados VARCHAR(50) DEFAULT NULL, -- Opcional
    horario TIME DEFAULT NULL,                 -- Opcional
    sesiones_por_mes INT DEFAULT NULL,         -- Opcional
    max_participantes INT DEFAULT NULL,        -- Opcional
    participantes_actuales INT DEFAULT 0,
    precio DECIMAL(10, 2) DEFAULT NULL,        -- Opcional
    activo BOOLEAN DEFAULT TRUE                -- Indica si la actividad está habilitada
);

-- Insertar actividades iniciales
INSERT INTO actividades (nombre)
VALUES
    ('Zumba'),
    ('Cycle'),
    ('Functional Boxing'),
    ('Dodgeball');

-- Tabla de inscripciones a actividades
CREATE TABLE inscripciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    socio_id INT NOT NULL,
    actividad_id INT NOT NULL,
    fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sesiones_restantes INT NOT NULL,
    FOREIGN KEY (socio_id) REFERENCES socios(id),
    FOREIGN KEY (actividad_id) REFERENCES actividades(id)
);

-- Tabla de asistencias
CREATE TABLE asistencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    socio_id INT NOT NULL,
    fecha DATE NOT NULL,
    tipo_ingreso ENUM('normal', 'gracia') DEFAULT 'normal',
    FOREIGN KEY (socio_id) REFERENCES socios(id)
);

-- Tabla de empleados
CREATE TABLE empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(15),
    direccion VARCHAR(255),
    puesto VARCHAR(50),
    password VARCHAR(255) NOT NULL
);
