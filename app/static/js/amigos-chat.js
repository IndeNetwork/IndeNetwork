document.addEventListener("DOMContentLoaded", () => {
    let messageInput = document.querySelector(".chat-input input");
    let sendButton = document.querySelector(".chat-input button");
    let messagesContainer = document.querySelector(".chat-messages");

    sendButton.addEventListener("click", () => {
        const messageText = messageInput.value.trim();
        if (messageText) {
            const messageElement = document.createElement("div");
            messageElement.classList.add("message", "sent");
            messageElement.innerHTML = `<p>${messageText}</p><span class="time">${new Date().toLocaleString()}</span>`;
            messagesContainer.appendChild(messageElement);
            messageInput.value = "";
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    });
});
