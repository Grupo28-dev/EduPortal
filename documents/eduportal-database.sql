CREATE DATABASE IF NOT EXISTS eduportal ;
USE eduportal ;

-- Crear la tabla de Roles

CREATE TABLE IF NOT EXISTS Rol (
    rol_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(100) NOT NULL,
    descripcion TEXT
) ENGINE=InnoDB;

-- Insertar roles predeterminados (admin, estandar, profesor, alumno) solo si no existen
INSERT INTO Rol (nombre_rol, descripcion) 
SELECT * FROM (SELECT 'admin', 'Rol para administradores') AS tmp
WHERE NOT EXISTS (SELECT nombre_rol FROM Rol WHERE nombre_rol = 'admin')
LIMIT 1;

INSERT INTO Rol (nombre_rol, descripcion) 
SELECT * FROM (SELECT 'estandar', 'Rol para usuarios estándar') AS tmp
WHERE NOT EXISTS (SELECT nombre_rol FROM Rol WHERE nombre_rol = 'estandar')
LIMIT 1;

INSERT INTO Rol (nombre_rol, descripcion) 
SELECT * FROM (SELECT 'profesor', 'Rol para profesores') AS tmp
WHERE NOT EXISTS (SELECT nombre_rol FROM Rol WHERE nombre_rol = 'profesor')
LIMIT 1;

INSERT INTO Rol (nombre_rol, descripcion) 
SELECT * FROM (SELECT 'alumno', 'Rol para alumnos') AS tmp
WHERE NOT EXISTS (SELECT nombre_rol FROM Rol WHERE nombre_rol = 'alumno')
LIMIT 1;

-- Crear la tabla Persona
CREATE TABLE IF NOT EXISTS Persona (
    id_persona INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    fecha_nacimiento DATE NOT NULL
) ENGINE=InnoDB;

-- Crear la tabla Usuario (relación con Rol y Persona)
CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    persona_id INT NOT NULL,
    rol_id INT NOT NULL,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,  -- Guardar la contraseña en texto plano
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (persona_id) REFERENCES Persona(id_persona),
    FOREIGN KEY (rol_id) REFERENCES Rol(rol_id)
) ENGINE=InnoDB;

-- Crear la tabla Alumno (con datos específicos del alumno)
CREATE TABLE IF NOT EXISTS Alumno (
    id_alumno INT AUTO_INCREMENT PRIMARY KEY,
    persona_id INT NOT NULL,
    matricula VARCHAR(50) NOT NULL,
    carrera VARCHAR(100) NOT NULL,
    semestre INT NOT NULL,
    fecha_ingreso DATE NOT NULL,
    becado BOOLEAN NOT NULL,
    FOREIGN KEY (persona_id) REFERENCES Persona(id_persona)
) ENGINE=InnoDB;

-- Crear la tabla Profesor (con datos específicos del profesor)
CREATE TABLE IF NOT EXISTS Profesor (
    id_profesor INT AUTO_INCREMENT PRIMARY KEY,
    persona_id INT NOT NULL,
    especialidad VARCHAR(100) NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    departamento VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    fecha_contratacion DATE NOT NULL,
    FOREIGN KEY (persona_id) REFERENCES Persona(id_persona)
) ENGINE=InnoDB;

-- Crear la tabla Curso
CREATE TABLE IF NOT EXISTS Curso (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    profesor_id INT,
    nombre_curso VARCHAR(100),
    descripcion TEXT,
    creditos INT,
    cupo_maximo INT,
    activo BOOLEAN,
    FOREIGN KEY (profesor_id) REFERENCES Profesor(id_profesor)
) ENGINE=InnoDB;

-- Crear la tabla Inscripcion
CREATE TABLE IF NOT EXISTS Inscripcion (
    id_inscripcion INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT,
    curso_id INT,
    fecha_inscripcion DATE,
    estado VARCHAR(50),
    FOREIGN KEY (alumno_id) REFERENCES Alumno(id_alumno),
    FOREIGN KEY (curso_id) REFERENCES Curso(id_curso)
) ENGINE=InnoDB;

-- Crear la tabla MetodoPago
CREATE TABLE IF NOT EXISTS MetodoPago (
    id_metodo_pago INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    activo BOOLEAN
) ENGINE=InnoDB;

-- Crear la tabla Calificacion
CREATE TABLE IF NOT EXISTS Calificacion (
    id_calificacion INT AUTO_INCREMENT PRIMARY KEY,
    inscripcion_id INT,
    nota DECIMAL(5,2),
    porcentaje DECIMAL(5,2),
    tipo_evaluacion VARCHAR(100),
    fecha_calificacion DATE,
    FOREIGN KEY (inscripcion_id) REFERENCES Inscripcion(id_inscripcion)
) ENGINE=InnoDB;

-- Crear la tabla Asistencia
CREATE TABLE IF NOT EXISTS Asistencia (
    id_asistencia INT AUTO_INCREMENT PRIMARY KEY,
    inscripcion_id INT,
    fecha DATE,
    presente BOOLEAN,
    observaciones TEXT,
    FOREIGN KEY (inscripcion_id) REFERENCES Inscripcion(id_inscripcion)
) ENGINE=InnoDB;

-- Crear la tabla Descuento
CREATE TABLE IF NOT EXISTS Descuento (
    id_descuento INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50),
    porcentaje DECIMAL(5,2),
    monto_fijo DECIMAL(10,2),
    fecha_inicio DATE,
    fecha_fin DATE,
    activo BOOLEAN
) ENGINE=InnoDB;

-- Crear la tabla Pago
CREATE TABLE IF NOT EXISTS Pago (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    inscripcion_id INT,
    metodo_pago_id INT,
    descuento_id INT,
    monto_total DECIMAL(10,2),
    monto_pagado DECIMAL(10,2),
    fecha_pago DATE,
    estado VARCHAR(50),
    comprobante VARCHAR(255),
    FOREIGN KEY (inscripcion_id) REFERENCES Inscripcion(id_inscripcion),
    FOREIGN KEY (metodo_pago_id) REFERENCES MetodoPago(id_metodo_pago),
    FOREIGN KEY (descuento_id) REFERENCES Descuento(id_descuento)
) ENGINE=InnoDB;-- Crear la base de datos


