
document.addEventListener("DOMContentLoaded", () => {
    let messageForm = document.getElementById("messageForm");
    let messageInput = document.querySelector(".chat-input input[name='Enter_mensaje']");
    let messagesContainer = document.querySelector(".chat-messages");
    let lastMessageTimestamp = null;
    const chatData = document.getElementById('chatData');
    const miembroActual = chatData ? parseInt(chatData.dataset.miembroActual) : null;

    let existingMessages = messagesContainer.querySelectorAll('.message');
if (existingMessages.length > 0) {
    let lastMessage = existingMessages[existingMessages.length - 1];
    lastMessageTimestamp = lastMessage.querySelector('.time').textContent;
}

if (miembroActual === null) {
    console.error('No se pudo obtener el ID del miembro actual');
}

    messageForm.addEventListener("submit", (e) => {
        e.preventDefault();

        const messageText = messageInput.value.trim();
        const formAction = messageForm.getAttribute("action");

        if (messageText) {
            sendMessage(messageText, formAction);
        }
    });

    function sendMessage(messageText, formAction) {
        const messageElement = addMessageToChat(messageText, 'sent');
    
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
                lastMessageTimestamp = new Date().toISOString(); // Añade esta línea
            } else {
                console.error(data.message);
                messageElement.classList.add("error");
                alert("Error al enviar el mensaje: " + data.message);
            }
        })
        .catch(error => {
            console.error("Error al enviar el mensaje:", error);
            messageElement.classList.add("error");
            alert("Error de conexión al enviar el mensaje");
        });
    
        messageInput.value = "";
    }
    function addMessageToChat(messageText, type) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", type);
        messageElement.innerHTML = `<p class="message-text">${messageText}</p><span class="${type}-time time">${new Date().toLocaleString()}</span>`;
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return messageElement;
    }

    
});

// Código para el buscador de amigos 
document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById('searchInput');
    const friendsList = document.getElementById('friendsList');
    const friends = friendsList.getElementsByTagName('li');

    const noResultsMessage = document.createElement('li');
    noResultsMessage.textContent = "Persona no existe";
    noResultsMessage.style.display = "none";
    friendsList.appendChild(noResultsMessage);

    searchInput.addEventListener('input', function() {
        const filter = searchInput.value.toLowerCase();
        let anyMatch = false;

        for (let i = 0; i < friends.length; i++) {
            const friendName = friends[i].innerText.toLowerCase();
            if (friendName.includes(filter)) {
                friends[i].style.display = "";
                anyMatch = true;
            } else {
                friends[i].style.display = "none";
            }
        }

        if (!anyMatch) {
            noResultsMessage.style.display = "";
        } else {
            noResultsMessage.style.display = "none";
        }
    });
});

function getNewMessages() {
    const amigoId = document.getElementById("amigo_id").value;
    fetch(`/get_new_messages/${amigoId}?ultimo_timestamp=${encodeURIComponent(lastMessageTimestamp)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                data.messages.forEach(mensaje => {
                    const tipo = mensaje[0] == miembroActual ? 'sent' : 'received';
                    addMessageToChat(mensaje[1], tipo);
                    lastMessageTimestamp = mensaje[2];
                });
            }
        })
        .catch(error => console.error("Error al obtener nuevos mensajes:", error));
}

setInterval(getNewMessages, 5000);