


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
  if (btnLogout) {
    btnLogout.addEventListener('click', function () {
      sessionStorage.removeItem('isLoggedIn');
      sessionStorage.removeItem('userEmail');
      window.location.href = './login.html';
      window.location.href = '../login.html';  // Redirige a la página de login
    });
  }
});
