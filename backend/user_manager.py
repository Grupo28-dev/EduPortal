# user_manager.py
from database import Database

class UserManager:
    def __init__(self):
        self.db = Database()

    # -----------------------------------------
    # Función para agregar un rol si no existe
    # -----------------------------------------
    def agregar_rol(self, nombre_rol, descripcion):
        """Crea un nuevo rol en la tabla Rol si no existe y devuelve el rol_id."""
        try:
            # Verificar si el rol ya existe
            sql_verificar_rol = "SELECT rol_id FROM Rol WHERE nombre_rol = %s"
            rol_result = self.db.query(sql_verificar_rol, (nombre_rol,))
            if rol_result:
                return rol_result[0]['rol_id']

            # Si no existe, crear el rol
            sql_crear_rol = "INSERT INTO Rol (nombre_rol, descripcion) VALUES (%s, %s)"
            self.db.execute(sql_crear_rol, (nombre_rol, descripcion))
            rol_id = self.db.last_insert_id()
            print(f"Rol '{nombre_rol}' creado exitosamente.")
            return rol_id
        except Exception as e:
            print(f"Error al crear el rol '{nombre_rol}': {e}")
            return None

    # -----------------------------------------
    # Registrar usuario
    # -----------------------------------------
    def registrar_usuario(self, nombre, apellido, email, contrasena, genero, telefono, rol='estandar', **datos_adicionales):
        """Registra un nuevo usuario, y si es alumno o profesor, registra sus datos específicos."""
        try:
            # Insertar persona
            sql_persona = """
                INSERT INTO Persona (nombre, apellido, email, telefono, fecha_nacimiento)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.db.execute(sql_persona, (
                nombre,
                apellido,
                email,
                telefono,
                datos_adicionales.get('fecha_nacimiento')
            ))

            # Obtener el persona_id
            persona_id = self.db.last_insert_id()

            # Verificar o crear rol
            rol_descripcion = ''
            if rol == 'admin':
                rol_descripcion = 'Rol para administradores'
            elif rol == 'estandar':
                rol_descripcion = 'Rol para usuarios estándar'
            elif rol == 'profesor':
                rol_descripcion = 'Rol para profesores'
            elif rol == 'alumno':
                rol_descripcion = 'Rol para alumnos'

            rol_id = self.agregar_rol(rol, rol_descripcion)
            if not rol_id:
                print(f"Error: no se pudo crear o encontrar el rol '{rol}'")
                return False

            # Insertar en Usuario
            sql_usuario = """
                INSERT INTO Usuario (persona_id, rol_id, username, password, activo)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.db.execute(sql_usuario, (persona_id, rol_id, email, contrasena, True))
            print(f"Usuario '{nombre} {apellido}' registrado con rol '{rol}'.")

            # Registrar datos específicos según rol
            if rol == 'alumno':
                self.registrar_alumno(datos_adicionales, persona_id)
            elif rol == 'profesor':
                self.registrar_profesor(datos_adicionales, persona_id)

            return True
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return False

    # -----------------------------------------
    # Registrar Alumno
    # -----------------------------------------
    def registrar_alumno(self, datos, persona_id):
        try:
            sql_alumno = """
                INSERT INTO Alumno (persona_id, matricula, carrera, semestre, fecha_ingreso, becado)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.db.execute(sql_alumno, (
                persona_id,
                datos['matricula'],
                datos['carrera'],
                datos['semestre'],
                datos['fecha_ingreso'],
                datos['becado']
            ))
            print(f"Alumno registrado: {datos['matricula']}")
        except Exception as e:
            print(f"Error al registrar el alumno: {e}")

    # -----------------------------------------
    # Registrar Profesor
    # -----------------------------------------
    def registrar_profesor(self, datos, persona_id):
        try:
            sql_profesor = """
                INSERT INTO Profesor (persona_id, especialidad, titulo, departamento, categoria, fecha_contratacion)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.db.execute(sql_profesor, (
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
        usuario = self.db.query(sql, (email,))

        if usuario:
            print(f"Usuario encontrado: {usuario[0]['username']}")
            if usuario[0]['password'] == contrasena:
                print("Inicio de sesión exitoso.")
                return usuario[0]
            else:
                print("Contraseña incorrecta.")
                return None
        else:
            print(f"No se encontró el usuario con email: {email}")
            return None

    # -----------------------------------------
    # Listar todos los usuarios
    # -----------------------------------------
    def listar_usuarios(self):
        sql = """
            SELECT u.id_usuario, u.username, r.nombre_rol
            FROM Usuario u
            JOIN Rol r ON u.rol_id = r.rol_id
        """
        return self.db.query(sql)

    # -----------------------------------------
    # Cambiar rol de usuario
    # -----------------------------------------
    def cambiar_rol_usuario(self, id_usuario, nuevo_rol):
        sql_rol = "SELECT rol_id FROM Rol WHERE nombre_rol = %s"
        rol_result = self.db.query(sql_rol, (nuevo_rol,))
        if not rol_result:
            print(f"Error: El rol '{nuevo_rol}' no existe.")
            return False
        rol_id = rol_result[0]['rol_id']

        sql = "UPDATE Usuario SET rol_id = %s WHERE id_usuario = %s"
        self.db.execute(sql, (rol_id, id_usuario))
        print(f"Rol del usuario {id_usuario} cambiado a '{nuevo_rol}'.")
        return True

    # -----------------------------------------
    # Eliminar usuario
    # -----------------------------------------
    def eliminar_usuario(self, id_usuario):
        sql = "DELETE FROM Usuario WHERE id_usuario = %s"
        self.db.execute(sql, (id_usuario,))
        print(f"Usuario {id_usuario} eliminado exitosamente.")
        return True
