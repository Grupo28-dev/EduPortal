
document.addEventListener("DOMContentLoaded", function () {
  // Verifica si los botones existen antes de añadir los event listeners
  const btnCursos = document.getElementById("btnCursos");
  const btnProfesores = document.getElementById("btnProfesores");
  const cursosSection = document.getElementById("cursosSection");
  const profesoresSection = document.getElementById("profesoresSection");

  if (btnCursos && btnProfesores && cursosSection && profesoresSection) {
    btnCursos.addEventListener("click", () => {
      cursosSection.classList.remove("d-none");
      profesoresSection.classList.add("d-none");
    });

    btnProfesores.addEventListener("click", () => {
      profesoresSection.classList.remove("d-none");
      cursosSection.classList.add("d-none");
    });
  }

  // ==================================================================
  // GESTIÓN DE SESIÓN Y VISIBILIDAD DE BOTONES
  // ==================================================================
  const btnLogin = document.getElementById('btnLogin');
  const btnRegistro = document.getElementById('btnRegistro'); // Botón dropdown de registro
  const btnLogout = document.getElementById('btnLogout');

  // Gestión de visibilidad de botones según el estado de sesión
  if (sessionStorage.getItem('isLoggedIn') === 'true') {
    if (btnLogin) btnLogin.style.display = 'none';
    if (btnRegistro) btnRegistro.parentElement.style.display = 'none'; // Oculta el <li> que contiene el dropdown
    if (btnLogout) btnLogout.style.display = 'block';

    // Lógica de Logout 
    if (btnLogout) {
      btnLogout.addEventListener('click', function () {
        sessionStorage.removeItem('isLoggedIn');
        sessionStorage.removeItem('userEmail');
        // Redirigimos a login
        window.location.href = window.location.pathname.includes('/pages/') ? '../login.html' : 'login.html';
      });
    }
  } else {
    // Si no está logueado, ocultar el botón de logout
    if (btnLogout) btnLogout.style.display = 'none';
  }

  // ==================================================================
  // LÓGICA UNIFICADA DE VALIDACIÓN DE FORMULARIOS
  // ==================================================================
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; //Expresiones regulares para validar el mail

  const handleFormSubmit = (form) => {
    if (!form) return;

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      event.stopPropagation();

      let isValid = true;
      const fields = form.querySelectorAll('input, select');

      // Limpiar validaciones previas
      fields.forEach(field => field.classList.remove('is-valid', 'is-invalid'));

      // Validar cada campo
      fields.forEach(field => {
        let fieldIsValid = true;
        const feedbackElement = field.nextElementSibling; // El field.nextElementSibling asume que el div de feedback está justo después (en nuestro código si, el feedback no-valid)

        // 1. Validación de campo requerido
        if (field.required && field.value.trim() === '') {
          if (feedbackElement) feedbackElement.textContent = 'Este campo es obligatorio.';
          fieldIsValid = false;
        }
        // 2. Validación de tipo email
        else if (field.type === 'email' && !emailRegex.test(field.value)) {
          if (feedbackElement) feedbackElement.textContent = 'Por favor, ingresa un correo electrónico válido.';
          fieldIsValid = false;
        }
        // 3. Validación de tipo date (no futura)
        else if (field.type === 'date' && new Date(field.value) > new Date()) {
          if (feedbackElement) feedbackElement.textContent = 'La fecha no puede ser futura.';
          fieldIsValid = false;
        }
        // 4. Validación de número (semestre > 0)
        else if (field.id === 'alumnoSemestre' && parseInt(field.value, 10) <= 0) {
          if (feedbackElement) feedbackElement.textContent = 'El semestre debe ser un número positivo.';
          fieldIsValid = false;
        }

        // Aplicar clases de Bootstrap
        if (fieldIsValid && field.value.trim() !== '') {
          field.classList.add('is-valid');
        } else if (!fieldIsValid) {
          field.classList.add('is-invalid');
          isValid = false; // Si un campo falla, todo el formulario es inválido
        }
      });

      if (isValid) {
        alert('Se registró con éxito');
        form.reset();
        fields.forEach(field => field.classList.remove('is-valid', 'is-invalid'));
      } else {
        alert('Error: Por favor, corrija los campos marcados en rojo.');
      }
    });
  };

  // Aplicar la lógica de validación a los formularios de registro
  handleFormSubmit(document.getElementById('formRegistroProfesor')); //O sea, importamos la función creada mas arriba handleFormSubmit para que se aplique al realizar una busqueda por id que coincida con el parametro
  handleFormSubmit(document.getElementById('formRegistroAlumno'));

  // ---  Formulario de Contacto ---
  const contactForm = document.getElementById('contactForm');

  if (contactForm) {
    contactForm.addEventListener('submit', function (event) {
      let isValid = true;
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      // Resetear validaciones previas
      contactForm.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
      contactForm.querySelectorAll('.is-valid').forEach(el => el.classList.remove('is-valid'));

      // Campos a validar
      const name = document.getElementById('name');
      const email = document.getElementById('email');
      const message = document.getElementById('message');

      // Validación de Nombre
      if (name.value.trim() === '') {
        name.classList.add('is-invalid');
        isValid = false;
      } else {
        name.classList.add('is-valid');
      }

      // Validación de Email
      if (!emailRegex.test(email.value)) {
        email.classList.add('is-invalid');
        isValid = false;
      } else {
        email.classList.add('is-valid');
      }

      // Validación de Mensaje
      if (message.value.trim() === '') {
        message.classList.add('is-invalid');
        isValid = false;
      } else {
        message.classList.add('is-valid');
      }

      if (isValid) {
        // Si todo es válido, oculta el formulario y muestra el mensaje
        contactForm.style.display = 'none';
        document.getElementById('thankYouMessage').style.display = 'block';
        // // Como es estatica no hay lógica, simulamos el envio con un mensaje. Aunque en pruebas no alcanza a mostrarse. Teorizamos que es por la carga casi instantanea del SMTP. Aunque para futuras integraciones de funcionalidades de respuesta debería funcionar
        console.log('Formulario válido, listo para enviar.');
      }
    });
  }
});
