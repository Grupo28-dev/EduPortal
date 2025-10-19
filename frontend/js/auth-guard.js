

// Verifica si el usuario ha iniciado sesión.
// Si no, lo redirige a la página de login.
// Esta comprobación debe estar en todas las páginas protegidas.

if (sessionStorage.getItem('isLoggedIn') !== 'true') {
    // Usamos una ruta relativa que funcione desde `index.html` y desde `pages/`.
    window.location.href = window.location.pathname.includes('/pages/') ? '../login.html' : 'login.html';
}