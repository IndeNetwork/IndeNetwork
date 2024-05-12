document.addEventListener("DOMContentLoaded", function () {
    document.querySelector(".animacion").style.display = "flex";
    document.querySelector(".contenedorFormulario").style.display = "none";
})

window.addEventListener("load", function () {
    setTimeout(function () {
        document.querySelector(".animacion").style.display = "none";
        document.querySelector(".contenedorFormulario").style.display = "block"
    }, 2000)
})
