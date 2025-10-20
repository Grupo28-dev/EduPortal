


document.addEventListener("DOMContentLoaded", function () {
  // Verificar si los botones existen antes de añadir los event listeners
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

  // Logout
  const btnLogout = document.getElementById('btnLogout');
  if (btnLogout) {   //NUEVO: Script de logout (verificación de sesiones)
    if (sessionStorage.getItem('isLoggedIn') === 'true') {
      // Si el usuario está logueado, el logout es visible y funciona
      btnLogout.style.display = 'block'; 
      btnLogout.addEventListener('click', function () {
        sessionStorage.removeItem('isLoggedIn');
        // Se borran los datos guardados en caché de la sesión y redirigimos a login
        window.location.href = window.location.pathname.includes('/pages/') ? '../login.html' : 'login.html';
      });
    } else {
      // Si el usuario no está logueado, el botón no aparece
      btnLogout.style.display = 'none';
    }
  }

  // --- Registro Profesor ---
  const formProfesor = document.getElementById('formRegistroProfesor');
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (formProfesor) {
    formProfesor.addEventListener('submit', function (event) {
      event.preventDefault();
      event.stopPropagation();

      let isValid = true;

      const validateField = (field) => {
        field.classList.remove('is-valid', 'is-invalid');
        if (field.value.trim() === '') {
          field.classList.add('is-invalid');
          return false;
        }
        field.classList.add('is-valid');
        return true;
      };

      const validateDateField = (field, feedbackElement) => {
        if (!validateField(field)) {
          feedbackElement.textContent = `El campo es obligatorio.`;
          return false;
        } else if (new Date(field.value) > new Date()) {
          field.classList.remove('is-valid');
          field.classList.add('is-invalid');
          feedbackElement.textContent = `La fecha no puede ser futura.`;
          return false;
        }
        return true;
      };

      const fieldsToValidate = ['profesorNombre', 'profesorApellido', 'profesorTelefono', 'profesorEspecialidad', 'profesorTitulo', 'profesorDepartamento', 'profesorCategoria'];
      fieldsToValidate.forEach(id => { isValid = validateField(document.getElementById(id)) && isValid; });

      isValid = validateDateField(document.getElementById('profesorFechaNacimiento'), document.getElementById('profesorFechaNacimiento').nextElementSibling) && isValid;
      isValid = validateDateField(document.getElementById('profesorFechaContrato'), document.getElementById('profesorFechaContrato').nextElementSibling) && isValid;

      const emailField = document.getElementById('profesorEmail');
      isValid = emailRegex.test(emailField.value) ? validateField(emailField) && isValid : (emailField.classList.add('is-invalid'), false);

      if (isValid) {
        console.log("Formulario de profesor es válido. Listo para enviar.");
      }
    });
  }

  // --- Registro  Alumno ---
  const formAlumno = document.getElementById('formRegistroAlumno');

  if (formAlumno) {
    formAlumno.addEventListener('submit', function (event) {
      event.preventDefault();
      event.stopPropagation();

      let isValid = true;

      // Función para validar un campo de texto simple
      const validateField = (field) => {
        field.classList.remove('is-valid', 'is-invalid');
        if (field.value.trim() === '') {
          field.classList.add('is-invalid');
          return false;
        }
        field.classList.add('is-valid');
        return true;
      };

      // Validar todos los campos
      isValid = validateField(document.getElementById('alumnoNombre')) && isValid;
      isValid = validateField(document.getElementById('alumnoApellido')) && isValid;
      isValid = validateField(document.getElementById('alumnoTelefono')) && isValid;
      isValid = validateField(document.getElementById('alumnoMatricula')) && isValid;
      isValid = validateField(document.getElementById('alumnoCarrera')) && isValid;

      // Validación de Fecha de Nacimiento
      const fechaNacimientoField = document.getElementById('alumnoFechaNacimiento');
      const fechaNacimientoFeedback = fechaNacimientoField.nextElementSibling;
      if (!validateField(fechaNacimientoField)) {
        fechaNacimientoFeedback.textContent = 'La fecha de nacimiento es obligatoria.';
        isValid = false;
      } else if (new Date(fechaNacimientoField.value) > new Date()) {
        fechaNacimientoField.classList.remove('is-valid');
        fechaNacimientoField.classList.add('is-invalid');
        fechaNacimientoFeedback.textContent = 'La fecha de nacimiento no puede ser futura.';
        isValid = false;
      }

      // Validación de Email
      const emailField = document.getElementById('alumnoEmail');
      isValid = emailRegex.test(emailField.value) ? validateField(emailField) && isValid : (emailField.classList.add('is-invalid'), false);

      // Validación de Semestre
      const semestreField = document.getElementById('alumnoSemestre');
      isValid = (semestreField.value > 0) ? validateField(semestreField) && isValid : (semestreField.classList.add('is-invalid'), false);

      if (isValid) {
        console.log("Formulario de alumno es válido. Listo para enviar.");
        // Como es estatica no hay lógica, simulamos el envio con un mensaje)
      }
    });
  }

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
        // // Como es estatica no hay lógica, simulamos el envio con un mensaje
        console.log('Formulario válido, listo para enviar.');
      }
    });
  }
});
