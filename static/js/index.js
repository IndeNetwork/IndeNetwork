document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("animacion").style.display = "flex"
    document.querySelector(".formulario").style.display = "none"
})

window.addEventListener("load", function () {
    setTimeout(function () {
        document.getElementById("animacion").style.display = "none"
        document.querySelector(".formulario").style.display = "flex"
    }, 1000)
    document.querySelector(".bttn_login").addEventListener("submit", function () {
        location.href = "login"
    })
})
