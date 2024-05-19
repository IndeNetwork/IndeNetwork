let refresh= document.getElementById('refresh')


refresh.addEventListener('click', function () {
    const img = this.querySelector('img');
    img.classList.add('spin-animation');
    setTimeout(() => {
        img.classList.remove('spin-animation');
    }, 1000); // La duración de la animación debe coincidir con el tiempo en CSS (1s en este caso)
});

refresh.addEventListener('click',function(){
    window.location.href = '/miembros/refresh'
});

function toggleOptions(button) {
    let optionsList = button.nextElementSibling;
    optionsList.classList.toggle('hidden');
}
