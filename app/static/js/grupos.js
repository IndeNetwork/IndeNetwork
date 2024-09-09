document.addEventListener("DOMContentLoaded", function () {
    // Inicio de la animacion del loader
    document.getElementById("body2").style.display = "none"
    document.querySelector(".animacion").style.display = "flex"
    localStorage.setItem("Documento", "{{documento}}")
})

window.addEventListener("load", function () {
    setTimeout(function () { //Duracion del animacion del loader
        document.querySelector(".animacion").style.display = "none"
        document.getElementById("body2").style.display = "block"
    }, 500)

    // Almacena el valor ingresado en el buscador de grupos
    const searchInput = document.getElementById("inputSearch_leftPanel")

    searchInput.addEventListener("keypress", function (event) { // Utiliza al Enter para enviar tambien los datos del formulario y ejcuta la funcion de busqueda.
        if (event.key === "Enter") {
            event.preventDefault() 
            realizarBusqueda()
        }
    })

    // Al realizarle click al boton de busqueda (El icono de lupa) ejecuta la funcion de la busqueda.
    document
        .getElementById("btnSearch_leftPanel")
        .addEventListener("click", function () {
            realizarBusqueda()
        })

    // Toma el id del icono de Refresh para ejecutar la recarga de la pagina.
    document
        .getElementById("refreshIMG_search")
        .addEventListener("click", function () {
            window.location.href = "/grupos"
        })
})

// Aqui se almacena la ruta de los archivos estaticos que seria: http://127.0.0.1:4000
const baseUrl = window.location.origin
console.log("URL:", baseUrl);

function realizarBusqueda() { // Esta es la funcion que realiza la busqueda, llamando a la funcion en python de la ruta "/grupos/search"
    
    const searchInput = document.getElementById("inputSearch_leftPanel").value
    fetch("/grupos/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: "grupo_aBuscar=" + encodeURIComponent(searchInput),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                alert(data.error)
            } else {
                // Si no se encuentra un error y todo funciona correctamente ejecuta la funcion que actualiza los datos en el html
                actualizarGrupos(data.grupos)
                actualizarMisGrupos(data.myGroups)
            }
        })
        .catch((error) => console.error("Error:", error))
}

function actualizarGrupos(grupos) { // Funcion para actualizar los datos en la pantalla (html)
    // Guarda o toma el id del div donde se mostraran los datos.
    const gruposList = document.querySelector("#totalGroups_leftPanel ul")
    gruposList.innerHTML = "" // Toma el div seleccionado anteriormente y lo formatea (le borra todo, queda el div vacio)
    // Verifica que lo devuelto por la funcion de python no este vacio
    if (grupos.length > 0) {
        // Pasa por cada registro o fila de la tupla "grupos" devuelta por la funcion de python
        grupos.forEach((grupo) => {
            // Crea una etiqueta "li"
            const li = document.createElement("li")
            // En la etiqueta "li" introduce los datos de la fila o el registro que toma en el forEach.
            li.innerHTML = `<p>${grupo[2]}°${grupo[3]} - ${grupo[1]}</p><a id="bttn-enterGroup" href="/grupos/insertar/${grupo[0]}"><img src="${baseUrl}/static/img/ICONS/EnterICO.svg" alt="" width="15" /></a>`
            gruposList.appendChild(li) // Ejecuta los cambios, es un tipo de Commit.
        })
    } else {
        // Si la funcion de python devuelve una tupla vacia introduce una etiqueta li donde se comunica que no se encontro ningun grupo.
        gruposList.innerHTML = `<li id="noGroups_leftPanel"><span style="color: gray;">No se han encontrado grupos con el nombre "${document.getElementById("inputSearch_leftPanel").value}"</span></li>`
    }
}

function actualizarMisGrupos(myGroups) { // Esta funcion actualiza los resultados de los datos pero para los grupos del miembroLogueado.
    const myGroupsList = document.querySelector("#myGroups_leftPanel ul") // Toma el Div
    myGroupsList.innerHTML = "" // Formatea el Div
    myGroups.forEach((grupo) => { // Pasa por cada fila de la tupla devuelta por la funcion de python.
        const li = document.createElement("li") // Crea un "li"
        // Introduce los valor devueltos por la funcion de python en la etiqueta "li"
        li.innerHTML = `<a href="#" onclick="obtenerTareas(${grupo[0]})">${grupo[2]}°${grupo[3]} - ${grupo[1]}<img src="${baseUrl}/static/img/ICONS/taskSearchICO.svg" alt="ICONO de ENLACE a GRUPO" width="15" /></a>`
        myGroupsList.appendChild(li) // Ejecuta los cambios, tipo de commit.
    })
}

/* FUNCION PARA PANEL DERECHO */
// Esta funcion es la encargada de mostrar los datos de cada grupo seleccionado dinamicamente,
function obtenerTareas(id_grupo) {

    fetch(`/grupos/view/${id_grupo}`, { // LLama la funcion de python para obtener su respuesta.
        method: "GET",
    })  
        // Aqui se verifica si hay una respuesta valida y si lo es devuelve la respuesta Json de la funcion de python.
        .then((response) => {
            if (!response.ok) {
                throw new Error("Error en la solicitud: " + response.statusText)
            }
            return response.json()
        })
        .then((data) => {
            // Toma el div donde se mostraran los resultados en el html.
            const content_rightPanel =
                document.getElementById("contentTask_rightPanel")
            content_rightPanel.innerHTML = "" // VAcia o formatea el div.

            data.forEach((tarea) => { // Se toma cada fila o registro devuelto en la tupla de la funcion de python 
                const div = document.createElement("div") // Se crea un div 
                // En el div se le incrusta una estructura html con los datos obtenidos de cada fila de la tupla analizada en el forEach.
                div.innerHTML = `
                <div id="content_rightPanel">
                    <div id="publicationInfo_rightPanel">
                        <div id="publicationUser_rightPanel">
                            <img
                                src="${baseUrl}/static/img/ICONS/UserCirculeICO.svg"
                                alt="Foto de Usuario"
                                width="30px"
                                title="Foto de Usuario"
                            />

                            <p><strong>${tarea[1]} ${tarea[2]}</strong></p>
                        </div>
                        <hr />
                        <p><small>${
                            new Date(tarea[6]).toLocaleDateString("es-ES") +
                            ", " +
                            new Date(tarea[6]).toLocaleTimeString("es-ES", {
                                hour: "2-digit",
                                minute: "2-digit",
                                hour12: true,
                            })
                        }</small></p>
                    </div>
                    <div id="publicationContent_rightPanel">
                        <h3>${tarea[3]}</h3>
                        <p>
                            ${tarea[4]}
                        </p>
                        <div id="contFile_publication">
                            <div id="file_publication">
                                <img
                                    src="${baseUrl}/static/img/ICONS/FileICO.svg"
                                    alt=""
                                />
                                <p>${tarea[5]}</p>
                            </div>
                            <img
                                src="${baseUrl}/static/img/ICONS/DownloadICO.svg"
                                alt=""
                                id="img_downloadFile"
                            />
                        </div>
                        <p><small>Fecha de vencimiento: ${
                            new Date(tarea[7]).toLocaleDateString("es-ES") +
                            ", " +
                            new Date(tarea[7]).toLocaleTimeString("es-ES", {
                                hour: "2-digit",
                                minute: "2-digit",
                                hour12: true,
                            })
                        }</small></p>
                        <p><small>Acceso a Comentarios: ${
                            tarea[8] === "SI" ? "Sí" : "No"
                        }</small></p>
                    </div>
                </div>
            `   
                content_rightPanel.appendChild(div) //Se aplican los cambios, (Se inserta el div creado en el div obtenido del html).
        })
    })
    
    .catch((error) => console.error("Error:", error))

    document.getElementById("btn_addTask").innerHTML = `
        {%if profesor%}
            <button id="aggTask">
                <img
                    src="${baseUrl}/static/img/ICONS/circle-plus.svg"
                    alt="Btn add task"
                />
            </button>
        {%endif%}`
}