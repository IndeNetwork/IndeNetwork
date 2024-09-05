// mensaje principal temporal
if (!sessionStorage.getItem('messageShown')) {
    swal.fire({
        icon: 'success',
        title: '¡Bienvenido a tu IndeChat!',
        text: 'Este es un espacio institucional. Por favor, mantén el respeto en todo momento.'
    });
    sessionStorage.setItem('messageShown', 'true');
}

// Selecciona todos los enlaces de la lista de amigos
const friendLinks = document.querySelectorAll('#friendsList a');

friendLinks.forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault();

        swal.fire({
            icon: 'success',
            title: 'Mensaje personalizado',
            text: `¿Quieres mandarle un mensaje a: ${link.textContent}?`,
            showCancelButton: true,
            confirmButtonText: 'Sí',
            cancelButtonText: 'No'
        }).then((result) => {
            if (result.isConfirmed) {
                // Si el usuario hizo clic en "Sí", redirigir al enlace
                window.location.href = link.href;
            }
            // Si el usuario hizo clic en "No", no hacer nada, se queda en la página
        });
    });
});

