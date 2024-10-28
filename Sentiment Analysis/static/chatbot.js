const socket = io.connect("http://localhost:5000");

//function to toggle chatbot
function toggleChatbot() {
    const chatbot = document.getElementById("chatbot");
    chatbot.style.display = chatbot.style.display === "none" ? "flex" : "none";
}

function sendMessage() {
    const userInput = document.getElementById("user-input"):
    const message = userInput.value;
    if (message.trim() !== "") {
        displayMessage("You", message);
        socket.emit("send_message", { message });
        userInput.value = "";
    }
}

socket.on("bot_response", (data) => {
    const botMessage = data.activities[0].text;
    displayMessage("Bot". botMessage)
});

function displayMessage(sender, message) {
    const messagesDiv = document.getElementById("chatbot-mesage");
    const messageDiv = document.createElement("div");
    messageDiv.textContent = `${sender}: ${message}`;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}