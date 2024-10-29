const socket = io.connect("http://localhost:5000");

//function to toggle chatbot
function toggleChatbot() {
    const chatbot = document.getElementById("chatbot");
    chatbot.style.display = chatbot.style.display === "none" ? "flex" : "none";
}

function sendMessage() {
    const userInput = document.getElementById("user_input");
    const message = userInput.value;
    if (message.trim() !== "") {
        displayMessage("You", message);
        socket.emit("send_message", { message });
        userInput.value = "";
    }
}

//listen for bot responses
socket.on("bot_response", (data) => {
    console.log("Received response from bot:", data)
    if (data.activities && data.activities.length > 0) {
        const botMessage = data.activities[0].text;
        displayMessage("Bot", botMessage)
    } else {
        displayMessage("Bot", "Bot did not respond")
    }
});

function displayMessage(sender, message) {
    const messagesDiv = document.getElementById("chatbot_messages");
    const messageDiv = document.createElement("div");
    messageDiv.textContent = `${sender}: ${message}`;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}