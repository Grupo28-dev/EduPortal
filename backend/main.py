# main.py
from user_manager import UserManager

def menu_principal():
    print("\n--- Sistema de Gestión de Usuarios ---")
    print("1. Registrar nuevo usuario")
    print("2. Iniciar sesión")
    print("3. Salir")

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
    print("4. Cerrar sesión")

def main():
    user_manager = UserManager()

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

            # Elegir el rol
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

            # Datos adicionales según el rol
            datos_adicionales = {'fecha_nacimiento': fecha_nacimiento}

            if rol == 'alumno':
                matricula = input("Matrícula: ")
                carrera = input("Carrera: ")
                semestre = input("Semestre: ")
                fecha_ingreso = input("Fecha de ingreso (YYYY-MM-DD): ")
                becado_input = input("¿Está becado? (True/False): ")
                becado = True if becado_input.strip().lower() == 'true' else False

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
                fecha_contratacion = input("Fecha de contratación (YYYY-MM-DD): ")

                datos_adicionales.update({
                    'especialidad': especialidad,
                    'titulo': titulo,
                    'departamento': departamento,
                    'categoria': categoria,
                    'fecha_contratacion': fecha_contratacion
                })

            # Registrar el usuario
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
                            for u in usuarios:
                                print(u)
                        elif opcion_admin == '2':
                            id_usuario = input("ID del usuario a cambiar rol: ")
                            nuevo_rol = input("Nuevo rol (estandar/admin/profesor/alumno): ")
                            user_manager.cambiar_rol_usuario(id_usuario, nuevo_rol)
                        elif opcion_admin == '3':
                            id_usuario = input("ID del usuario a eliminar: ")
                            user_manager.eliminar_usuario(id_usuario)
                        elif opcion_admin == '4':
                            print("Cerrando sesión de administrador.")
                            break
                        else:
                            print("Opción no válida.")
                else:  # Usuarios estándar, profesor o alumno
                    while True:
                        menu_usuario()
                        opcion_usuario = input("Seleccione una opción: ")
                        if opcion_usuario == '1':
                            print(f"\nDatos de usuario: {usuario}")
                        elif opcion_usuario == '2':
                            print("Funcionalidad de edición no implementada en este sprint.")
                        elif opcion_usuario == '3':
                            print("Cerrando sesión de usuario.")
                            break
                        else:
                            print("Opción no válida.")
        elif opcion == '3':
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
