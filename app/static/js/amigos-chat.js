document.addEventListener("DOMContentLoaded", () => {
    // Obtención del formulario de mensajes y elementos relacionados
    let messageForm = document.getElementById("messageForm");
    let messageInput = document.querySelector(".chat-input input[name='Enter_mensaje']");
    let messagesContainer = document.querySelector(".chat-messages");

    // Manejo del envío del formulario
    messageForm.addEventListener("submit", (e) => {
        e.preventDefault(); // Previene la submisión normal del formulario

        const messageText = messageInput.value.trim();
        const formAction = messageForm.getAttribute("action");

        if (messageText) {
            // Creación del nuevo mensaje en el DOM
            const messageElement = document.createElement("div");
            messageElement.classList.add("message", "sent");
            messageElement.innerHTML = `<p class="message-text">${messageText}</p><span class="sent-time time">${new Date().toLocaleString()}</span>`;
            messagesContainer.appendChild(messageElement);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;

            // Envío del mensaje al servidor usando Fetch API
            fetch(formAction, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: `Enter_mensaje=${encodeURIComponent(messageText)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log(data.message);
                    // aqui se puede actualizar la UI si es necesario
                } else {
                    console.error(data.message);
                    alert("Error al enviar el mensaje: " + data.message);
                }
            })
            .catch(error => {
                console.error("Error al enviar el mensaje:", error);
                alert("Error de conexión al enviar el mensaje");
            });

            // Limpiar el campo de entrada después de enviar el mensaje
            messageInput.value = "";
        }
    });
});
