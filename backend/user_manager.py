
from dataclasses import dataclass
from typing import List, Optional
from database import Database


# ---------- (POO) ----------
@dataclass
class Curso:
    id_curso: int
    nombre: str


@dataclass
class Usuario:
    id_usuario: int
    username: str
    rol: str


@dataclass
class Alumno:
    persona_id: int
    matricula: str
    carrera: str
    semestre: int
    curso: Optional[Curso] = None


class UserManager:
    def __init__(self):
        self._db = Database()

    # -----------------------------------------
    # (privado) Agregar rol si no existe
    # -----------------------------------------

    def _agregar_rol(self, nombre_rol, descripcion):
        try:
            sql_verificar_rol = "SELECT rol_id FROM Rol WHERE nombre_rol = %s"
            rol_result = self._db.query(sql_verificar_rol, (nombre_rol,))
            if rol_result:
                return rol_result[0]['rol_id']

            sql_crear_rol = "INSERT INTO Rol (nombre_rol, descripcion) VALUES (%s, %s)"
            self._db.execute(sql_crear_rol, (nombre_rol, descripcion))
            rol_id = self._db.last_insert_id()
            print(f"Rol '{nombre_rol}' creado exitosamente.")
            return rol_id
        except Exception as e:
            print(f"Error al crear el rol '{nombre_rol}': {e}")
            return None

    # -----------------------------------------
    # Sembrar cursos por defecto (idempotente)
    # -----------------------------------------

    def seed_cursos_por_defecto(self):
        cursos = [
            "Curso de HTML y CSS",
            "JavaScript Básico",
            "React para Principiantes",
            "Python desde Cero",
            "Bases de Datos MySQL",
            "Git y GitHub"
        ]
        try:
            for nombre in cursos:
                existe = self._db.query(
                    "SELECT id_curso FROM Curso WHERE nombre = %s", (nombre,))
                if not existe:
                    self._db.execute(
                        "INSERT INTO Curso (nombre) VALUES (%s)", (nombre,))
        except Exception as e:
            print(f"Error al sembrar cursos: {e}")

    # -----------------------------------------
    # Listar cursos (POO -> objetos Curso)
    # -----------------------------------------

    def obtener_cursos(self) -> List[Curso]:
        filas = self._db.query(
            "SELECT id_curso, nombre FROM Curso ORDER BY nombre")
        if not filas:
            return []
        return [Curso(id_curso=f["id_curso"], nombre=f["nombre"]) for f in filas]

    # -----------------------------------------
    # Registrar usuario (POO)
    # -----------------------------------------

    def registrar_usuario(self, nombre, apellido, email, contrasena, genero, telefono, rol='estandar', **datos_adicionales):
        try:
            # Insertar persona
            sql_persona = """
                INSERT INTO Persona (nombre, apellido, email, telefono, fecha_nacimiento)
                VALUES (%s, %s, %s, %s, %s)
            """
            self._db.execute(sql_persona, (
                nombre,
                apellido,
                email,
                telefono,
                datos_adicionales.get('fecha_nacimiento')
            ))
            persona_id = self._db.last_insert_id()

            # Rol
            rol_descripcion = {
                'admin': 'Rol para administradores',
                'estandar': 'Rol para usuarios estándar',
                'profesor': 'Rol para profesores',
                'alumno': 'Rol para alumnos'
            }.get(rol, 'Rol para usuarios estándar')

            rol_id = self._agregar_rol(rol, rol_descripcion)
            if not rol_id:
                print(f"Error: no se pudo crear o encontrar el rol '{rol}'")
                return False

            # Usuario
            sql_usuario = """
                INSERT INTO Usuario (persona_id, rol_id, username, password, activo)
                VALUES (%s, %s, %s, %s, %s)
            """
            self._db.execute(
                sql_usuario, (persona_id, rol_id, email, contrasena, True))
            print(f"Usuario '{nombre} {apellido}' registrado con rol '{rol}'.")

            # Datos específicos
            if rol == 'alumno':
                self._registrar_alumno(datos_adicionales, persona_id)
                # Inscribir al curso si vino curso_id
                curso_id = datos_adicionales.get('curso_id')
                if curso_id:
                    self.registrar_inscripcion_alumno(persona_id, curso_id)

            elif rol == 'profesor':
                self._registrar_profesor(datos_adicionales, persona_id)

            return True
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return False

    # -----------------------------------------
    # (privado) Registrar Alumno
    # -----------------------------------------

    def _registrar_alumno(self, datos, persona_id):
        try:
            sql_alumno = """
                INSERT INTO Alumno (persona_id, matricula, carrera, semestre, fecha_ingreso, becado)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self._db.execute(sql_alumno, (
                persona_id,
                datos['matricula'],
                datos['carrera'],
                int(datos['semestre']),
                datos['fecha_ingreso'],
                bool(datos['becado'])
            ))
            print(f"Alumno registrado: {datos['matricula']}")
        except Exception as e:
            print(f"Error al registrar el alumno: {e}")

    # -----------------------------------------
    # (privado) Registrar Profesor
    # -----------------------------------------

    def _registrar_profesor(self, datos, persona_id):
        try:
            sql_profesor = """
                INSERT INTO Profesor (persona_id, especialidad, titulo, departamento, categoria, fecha_contratacion)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self._db.execute(sql_profesor, (
                persona_id,
                datos['especialidad'],
                datos['titulo'],
                datos['departamento'],
                datos['categoria'],
                datos['fecha_contratacion']
            ))
            print(f"Profesor registrado: {datos['titulo']}")
        except Exception as e:
            print(f"Error al registrar el profesor: {e}")

    # -----------------------------------------
    # Inscribir Alumno en Curso (tabla puente)
    # -----------------------------------------

    def registrar_inscripcion_alumno(self, persona_id: int, curso_id: int):
        try:
            # Usamos la tabla Alumno_Curso con persona_id, como solicitaste.
            existe = self._db.query(
                "SELECT 1 FROM Alumno_Curso WHERE persona_id = %s AND curso_id = %s", (persona_id, curso_id))
            if not existe:
                self._db.execute(
                    "INSERT INTO Alumno_Curso (persona_id, curso_id) VALUES (%s, %s)", (persona_id, curso_id))
                print(
                    f"Alumno con persona_id {persona_id} inscripto en curso {curso_id}.")
        except Exception as e:
            print(f"Error al inscribir alumno en curso: {e}")

    # -----------------------------------------
    # Iniciar sesión
    # -----------------------------------------

    def iniciar_sesion(self, email, contrasena):
        sql = """
            SELECT u.id_usuario, u.username, u.password, r.nombre_rol
            FROM Usuario u
            JOIN Persona p ON u.persona_id = p.id_persona
            JOIN Rol r ON u.rol_id = r.rol_id
            WHERE p.email = %s
        """
        usuario = self._db.query(sql, (email,))
        if usuario:
            print(f"Usuario encontrado: {usuario[0]['username']}")
            if usuario[0]['password'] == contrasena:
                print("Inicio de sesión exitoso.")
                return usuario[0]
            print("Contraseña incorrecta.")
        else:
            print(f"No se encontró el usuario con email: {email}")
        return None

    # -----------------------------------------
    # Obtener detalles completos de un usuario
    # -----------------------------------------

    def obtener_detalles_usuario(self, id_usuario: int):
        # 1. Obtener persona_id y rol desde el id_usuario
        sql_base = "SELECT persona_id, rol_id FROM Usuario WHERE id_usuario = %s"
        user_base = self._db.query(sql_base, (id_usuario,))
        if not user_base:
            return {"error": "Usuario no encontrado"}

        persona_id = user_base[0]['persona_id']

        # 2. Obtener datos de la tabla Persona
        sql_persona = "SELECT p.*, r.nombre_rol FROM Persona p JOIN Usuario u ON p.id_persona = u.persona_id JOIN Rol r ON u.rol_id = r.rol_id WHERE p.id_persona = %s"
        datos_completos = self._db.query(sql_persona, (persona_id,))[0]

        rol = datos_completos['nombre_rol']

        # 3. Si es alumno, agregar datos de Alumno y Curso
        if rol == 'alumno':
            sql_alumno = """
                SELECT a.matricula, a.carrera, a.semestre, a.fecha_ingreso, a.becado
                FROM Alumno a
                WHERE a.persona_id = %s
            """
            datos_alumno = self._db.query(sql_alumno, (persona_id,))
            if datos_alumno:
                datos_completos.update(datos_alumno[0])

            # Obtener TODOS los cursos inscritos
            sql_cursos = """
                SELECT c.nombre
                FROM Curso c
                JOIN Alumno_Curso ac ON c.id_curso = ac.curso_id
                WHERE ac.persona_id = %s
            """
            cursos_inscritos = self._db.query(sql_cursos, (persona_id,))
            datos_completos['cursos_inscritos'] = [curso['nombre']
                                                   for curso in cursos_inscritos] if cursos_inscritos else ["(Ninguno)"]

        # 4. Si es profesor, agregar datos de Profesor
        elif rol == 'profesor':
            sql_profesor = "SELECT * FROM Profesor WHERE persona_id = %s"
            datos_profesor = self._db.query(sql_profesor, (persona_id,))
            if datos_profesor:
                # Excluimos persona_id para no duplicarlo
                prof_data = {
                    k: v for k, v in datos_profesor[0].items() if k != 'persona_id'}
                datos_completos.update(prof_data)

        # Limpiar datos no necesarios para la vista del usuario
        datos_completos.pop('id_persona', None)

        return datos_completos

    # -----------------------------------------
    # Listar todos los usuarios
    # -----------------------------------------

    def listar_usuarios(self):
        sql = """
            SELECT u.id_usuario, u.username, r.nombre_rol
            FROM Usuario u
            JOIN Rol r ON u.rol_id = r.rol_id
        """
        return self._db.query(sql)

    # -----------------------------------------
    # Cambiar rol
    # -----------------------------------------

    def cambiar_rol_usuario(self, id_usuario, nuevo_rol):
        sql_rol = "SELECT rol_id FROM Rol WHERE nombre_rol = %s"
        rol_result = self._db.query(sql_rol, (nuevo_rol,))
        if not rol_result:
            print(f"Error: El rol '{nuevo_rol}' no existe.")
            return False
        rol_id = rol_result[0]['rol_id']

        sql = "UPDATE Usuario SET rol_id = %s WHERE id_usuario = %s"
        self._db.execute(sql, (rol_id, id_usuario))
        print(f"Rol del usuario {id_usuario} cambiado a '{nuevo_rol}'.")
        return True

    # -----------------------------------------
    # Eliminar usuario
    # -----------------------------------------

    def eliminar_usuario(self, id_usuario):
        sql = "DELETE FROM Usuario WHERE id_usuario = %s"
        self._db.execute(sql, (id_usuario,))
        print(f"Usuario {id_usuario} eliminado exitosamente.")
        return True

    # -----------------------------------------
    # JOIN: Alumnos + Cursos (para listado por consola)
    # -----------------------------------------

    def listar_alumnos_con_curso(self):
        sql = """
        SELECT
            p.id_persona,
            p.nombre,
            p.apellido,
            a.matricula,
            a.carrera,
            a.semestre,
            c.id_curso,
            c.nombre AS nombre_curso
        FROM Persona p
        JOIN Alumno a ON p.id_persona = a.persona_id
        LEFT JOIN Alumno_Curso ac ON p.id_persona = ac.persona_id
        LEFT JOIN Curso c ON c.id_curso = ac.curso_id
        ORDER BY p.apellido, p.nombre
        """
        return self._db.query(sql)
