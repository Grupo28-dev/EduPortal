 const btnCursos = document.getElementById("btnCursos");
    const btnProfesores = document.getElementById("btnProfesores");
    const cursosSection = document.getElementById("cursosSection");
    const profesoresSection = document.getElementById("profesoresSection");

    btnCursos.addEventListener("click", () => {
      cursosSection.classList.remove("d-none");
      profesoresSection.classList.add("d-none");
    });

    btnProfesores.addEventListener("click", () => {
      profesoresSection.classList.remove("d-none");
      cursosSection.classList.add("d-none");
    });