//function to toggle chatbot
function toggleChatbot() {
    const chatbot = document.getElementById("chatbot");
    chatbot.style.display = chatbot.style.display === "none" ? "flex" : "none";
}

//function to handle 'enter'
function handleEnter(event) {
    if(event.key === "Enter") {
        sendMessage();
    }
}

//function to handle sending a message
function sendMessage() {
    const userInput = document.getElementById("user_input").value;
    if(userInput.trim() === "") return;

    //display user message in the chatbox
    const chatBotMessages = document.getElementById("chatbot_messages");
    chatBotMessages.innerHTML += `<div><strong>Term:</strong> ${userInput}</div>`;

    //clear input field
    document.getElementById("user_input").value = "";

    //send message to the server 
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        chatBotMessages.innerHTML += `&nbsp;<div><strong>Definition:</strong></br>${data.response}</div>&nbsp;`;
        chatBotMessages.scrollTop = chatBotMessages.scrollHeight;
    })
    .catch(error => console.error("Error:", error))
}