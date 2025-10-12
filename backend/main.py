
from user_manager import UserManager


def menu_principal():
    print("\n--- Sistema de Gestión de Usuarios ---")
    print("1. Registrar nuevo usuario")
    print("2. Iniciar sesión")
    # --- NUEVO ---
    print("3. Ver Cursos")          
    print("4. Salir")


def menu_usuario():
    print("\n--- Menú de Usuario ---")
    print("1. Ver mis datos")
    print("2. Editar mis datos (No implementado en este sprint)")
    print("3. Cerrar sesión")


def menu_admin():
    print("\n--- Menú de Administrador ---")
    print("1. Listar todos los usuarios")
    print("2. Cambiar rol de un usuario")
    print("3. Eliminar usuario")
    # --- NUEVO ---
    print("4. Listar alumnos + curso (JOIN)")  
    print("5. Cerrar sesión")


def main():
    user_manager = UserManager()
    # Asegura que los cursos base existan
    user_manager.seed_cursos_por_defecto()

    while True:
        menu_principal()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Registro de nuevo usuario
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            email = input("Email: ")
            contrasena = input("Contraseña: ")
            genero = input("Género: ")
            telefono = input("Teléfono: ")
            fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")

            # Elegir rol
            print("\nSeleccione el rol para el nuevo usuario:")
            print("1. Admin")
            print("2. Estándar")
            print("3. Profesor")
            print("4. Alumno")
            rol_op = input("Seleccione una opción: ")

            if rol_op == '1':
                rol = 'admin'
            elif rol_op == '2':
                rol = 'estandar'
            elif rol_op == '3':
                rol = 'profesor'
            elif rol_op == '4':
                rol = 'alumno'
            else:
                print("Opción no válida. Se asignará el rol 'estandar'.")
                rol = 'estandar'

            datos_adicionales = {'fecha_nacimiento': fecha_nacimiento}

            if rol == 'alumno':
                matricula = input("Matrícula: ")
                carrera = input("Carrera: ")
                semestre = input("Semestre: ")
                fecha_ingreso = input("Fecha de ingreso (YYYY-MM-DD): ")
                becado_input = input("¿Está becado? (True/False): ")
                becado = True if becado_input.strip().lower() == 'true' else False

                # --- SELECCIÓN DE CURSO POR CONSOLA ---
                cursos = user_manager.obtener_cursos()
                if not cursos:
                    print("No hay cursos disponibles. Contacte al admin.")
                else:
                    print("\nSeleccione un curso para inscribirse:")
                    for idx, c in enumerate(cursos, start=1):
                        print(f"{idx}. {c.nombre}")
                    try:
                        sel = int(input("Opción: "))
                        if 1 <= sel <= len(cursos):
                            curso_id = cursos[sel - 1].id_curso
                            datos_adicionales['curso_id'] = curso_id
                        else:
                            print("Selección inválida. No se inscribirá a un curso.")
                    except ValueError:
                        print("Entrada inválida. No se inscribirá a un curso.")

                datos_adicionales.update({
                    'matricula': matricula,
                    'carrera': carrera,
                    'semestre': int(semestre),
                    'fecha_ingreso': fecha_ingreso,
                    'becado': becado
                })

            elif rol == 'profesor':
                especialidad = input("Especialidad: ")
                titulo = input("Título: ")
                departamento = input("Departamento: ")
                categoria = input("Categoría: ")
                fecha_contratacion = input(
                    "Fecha de contratación (YYYY-MM-DD): ")

                datos_adicionales.update({
                    'especialidad': especialidad,
                    'titulo': titulo,
                    'departamento': departamento,
                    'categoria': categoria,
                    'fecha_contratacion': fecha_contratacion
                })

            user_manager.registrar_usuario(
                nombre, apellido, email, contrasena, genero, telefono, rol,
                **datos_adicionales
            )

        elif opcion == '2':
            # Login
            email = input("Email: ")
            contrasena = input("Contraseña: ")
            usuario = user_manager.iniciar_sesion(email, contrasena)

            if usuario:
                if usuario['nombre_rol'] == 'admin':
                    while True:
                        menu_admin()
                        opcion_admin = input("Seleccione una opción: ")
                        if opcion_admin == '1':
                            usuarios = user_manager.listar_usuarios()
                            for u in usuarios or []:
                                print(u)
                        elif opcion_admin == '2':
                            id_usuario = input(
                                "ID del usuario a cambiar rol: ")
                            nuevo_rol = input(
                                "Nuevo rol (estandar/admin/profesor/alumno): ")
                            user_manager.cambiar_rol_usuario(
                                id_usuario, nuevo_rol)
                        elif opcion_admin == '3':
                            id_usuario = input("ID del usuario a eliminar: ")
                            user_manager.eliminar_usuario(id_usuario)
                        elif opcion_admin == '4':  # JOIN alumnos + curso
                            filas = user_manager.listar_alumnos_con_curso()
                            if not filas:
                                print("No hay alumnos/cursos para mostrar.")
                            else:
                                print("\n--- Alumnos + Curso ---")
                                for f in filas:
                                    nom_curso = f['nombre_curso'] or "(sin curso)"
                                    print(
                                        f"{f['apellido']}, {f['nombre']} - Mat: {f['matricula']} - Carrera: {f['carrera']} - Sem: {f['semestre']} - Curso: {nom_curso}")
                        elif opcion_admin == '5':
                            print("Cerrando sesión de administrador.")
                            break
                        else:
                            print("Opción no válida.")
                else:
                    while True:
                        menu_usuario()
                        opcion_usuario = input("Seleccione una opción: ")
                        if opcion_usuario == '1':
                            # Usamos la nueva función para obtener todos los detalles
                            detalles = user_manager.obtener_detalles_usuario(
                                usuario['id_usuario'])
                            print("\n--- Mis Datos ---")
                            for clave, valor in detalles.items():
                                # Formateamos un poco la salida para que sea más legible
                                if clave == 'cursos_inscritos':
                                    print(
                                        f"Cursos inscritos: {', '.join(valor)}")
                                else:
                                    clave_formateada = clave.replace(
                                        '_', ' ').capitalize()
                                    print(f"{clave_formateada}: {valor}")
                        elif opcion_usuario == '2':
                            print(
                                "Funcionalidad de edición no implementada en este sprint.")
                        elif opcion_usuario == '3':
                            print("Cerrando sesión de usuario.")
                            break
                        else:
                            print("Opción no válida.")

        elif opcion == '3':
            # Ver cursos (sin login)
            cursos = user_manager.obtener_cursos()
            if not cursos:
                print("No hay cursos cargados.")
            else:
                print("\n--- Cursos Disponibles ---")
                for c in cursos:
                    print(f"- {c.nombre}")

        elif opcion == '4':
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")


if __name__ == "__main__":
    main()
