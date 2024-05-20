let refresh= document.getElementById('refresh')
let btn_insertar = document.querySelector('.btn-insert')
let btn_edit= document.getElementById('btn-edit')
let btn_delete = document.getElementById('btn-delete')

refresh.addEventListener('click', function () {
    const img = this.querySelector('img');
    img.classList.add('spin-animation');
    setTimeout(() => {
        img.classList.remove('spin-animation');
    }, 1000);
});

refresh.addEventListener('click',function(){
    window.location.href = '/miembros/refresh'
});

function toggleOptions(button) {
    let optionsList = button.nextElementSibling;
    optionsList.classList.toggle('hidden');
}


document.getElementById('Cancelar').addEventListener('click', function(){
    var element = document.getElementById('insertar');
    
    if (element.classList.contains('hidden')) {
        element.classList.remove('hidden');
        element.offsetHeight;
        element.classList.add('visible');
    } else {
        element.classList.remove('visible');
        setTimeout(() => {
            element.classList.add('hidden');
        }, 1000)
    }   
})

btn_insertar.addEventListener('click', function () {
    var element = document.getElementById('insertar');
    
    if (element.classList.contains('hidden')) {
        element.classList.remove('hidden');
        element.offsetHeight;
        element.classList.add('visible');
    } else {
        element.classList.remove('visible');
        setTimeout(() => {
            element.classList.add('hidden');
        }, 1000);
    }
});
