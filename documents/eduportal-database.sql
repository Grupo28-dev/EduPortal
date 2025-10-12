-- Base de datos
CREATE DATABASE IF NOT EXISTS eduportal
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_0900_ai_ci;
USE eduportal;

-- Rol
CREATE TABLE IF NOT EXISTS Rol (
  rol_id INT AUTO_INCREMENT PRIMARY KEY,
  nombre_rol VARCHAR(100) NOT NULL UNIQUE,
  descripcion TEXT
) ENGINE=InnoDB;

INSERT INTO Rol (nombre_rol, descripcion)
SELECT 'admin', 'Rol para administradores'
WHERE NOT EXISTS (SELECT 1 FROM Rol WHERE nombre_rol='admin');

INSERT INTO Rol (nombre_rol, descripcion)
SELECT 'estandar', 'Rol para usuarios estándar'
WHERE NOT EXISTS (SELECT 1 FROM Rol WHERE nombre_rol='estandar');

INSERT INTO Rol (nombre_rol, descripcion)
SELECT 'profesor', 'Rol para profesores'
WHERE NOT EXISTS (SELECT 1 FROM Rol WHERE nombre_rol='profesor');

INSERT INTO Rol (nombre_rol, descripcion)
SELECT 'alumno', 'Rol para alumnos'
WHERE NOT EXISTS (SELECT 1 FROM Rol WHERE nombre_rol='alumno');

-- Persona
CREATE TABLE IF NOT EXISTS Persona (
  id_persona INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  apellido VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  telefono VARCHAR(20) NOT NULL,
  fecha_nacimiento DATE NOT NULL
) ENGINE=InnoDB;

-- Usuario
CREATE TABLE IF NOT EXISTS Usuario (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  persona_id INT NOT NULL,
  rol_id INT NOT NULL,
  username VARCHAR(100) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  activo BOOLEAN NOT NULL DEFAULT TRUE,
  CONSTRAINT fk_usuario_persona
    FOREIGN KEY (persona_id) REFERENCES Persona(id_persona)
    ON DELETE CASCADE,
  CONSTRAINT fk_usuario_rol
    FOREIGN KEY (rol_id) REFERENCES Rol(rol_id)
    ON DELETE RESTRICT
) ENGINE=InnoDB;

-- Alumno (PK = persona_id)
CREATE TABLE IF NOT EXISTS Alumno (
  persona_id INT PRIMARY KEY,
  matricula VARCHAR(50) NOT NULL,
  carrera VARCHAR(100) NOT NULL,
  semestre INT NOT NULL,
  fecha_ingreso DATE NOT NULL,
  becado BOOLEAN NOT NULL,
  CONSTRAINT fk_alumno_persona
    FOREIGN KEY (persona_id) REFERENCES Persona(id_persona)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- Profesor (PK = persona_id)
CREATE TABLE IF NOT EXISTS Profesor (
  persona_id INT PRIMARY KEY,
  especialidad VARCHAR(100) NOT NULL,
  titulo VARCHAR(100) NOT NULL,
  departamento VARCHAR(100) NOT NULL,
  categoria VARCHAR(50) NOT NULL,
  fecha_contratacion DATE NOT NULL,
  CONSTRAINT fk_profesor_persona
    FOREIGN KEY (persona_id) REFERENCES Persona(id_persona)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- Curso (campo 'nombre' exacto)
CREATE TABLE IF NOT EXISTS Curso (
  id_curso INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- Seed de cursos
INSERT INTO Curso (nombre)
SELECT 'Curso de HTML y CSS'
WHERE NOT EXISTS (SELECT 1 FROM Curso WHERE nombre='Curso de HTML y CSS');
INSERT INTO Curso (nombre)
SELECT 'JavaScript Básico'
WHERE NOT EXISTS (SELECT 1 FROM Curso WHERE nombre='JavaScript Básico');
INSERT INTO Curso (nombre)
SELECT 'React para Principiantes'
WHERE NOT EXISTS (SELECT 1 FROM Curso WHERE nombre='React para Principiantes');
INSERT INTO Curso (nombre)
SELECT 'Python desde Cero'
WHERE NOT EXISTS (SELECT 1 FROM Curso WHERE nombre='Python desde Cero');
INSERT INTO Curso (nombre)
SELECT 'Bases de Datos MySQL'
WHERE NOT EXISTS (SELECT 1 FROM Curso WHERE nombre='Bases de Datos MySQL');
INSERT INTO Curso (nombre)
SELECT 'Git y GitHub'
WHERE NOT EXISTS (SELECT 1 FROM Curso WHERE nombre='Git y GitHub');

-- Puente Alumno_Curso
CREATE TABLE IF NOT EXISTS Alumno_Curso (
  persona_id INT NOT NULL,
  curso_id INT NOT NULL,
  PRIMARY KEY (persona_id, curso_id),
  CONSTRAINT fk_ac_alumno
    FOREIGN KEY (persona_id) REFERENCES Alumno(persona_id)
    ON DELETE CASCADE,
  CONSTRAINT fk_ac_curso
    FOREIGN KEY (curso_id) REFERENCES Curso(id_curso)
    ON DELETE CASCADE
) ENGINE=InnoDB;



