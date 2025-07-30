
// Handle form submission
document.getElementById("chat-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    // Get user input
    const userInput = document.getElementById("user-input").value.trim();
    if (!userInput) return;

    // Display the user's message
    displayMessage(userInput, "user-message");

    // Clear input field
    document.getElementById("user-input").value = "";

    // Add a "typing" indicator
    const chatbox = document.getElementById("chatbox");
    const typingIndicator = document.createElement("div");
    typingIndicator.className = "bot-message typing-indicator";
    typingIndicator.innerHTML = `<span class="avatar">🤖</span> <p>Typing...</p>`;
    chatbox.appendChild(typingIndicator);
    chatbox.scrollTop = chatbox.scrollHeight;

    // Fetch bot response
    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: userInput }),
        });

        const data = await response.json();

        // Remove typing indicator
        chatbox.removeChild(typingIndicator);

        // Display the bot's message
        displayMessage(data.reply, "bot-message");
    } catch (error) {
        console.error("Error:", error);

        // Remove typing indicator and display error
        chatbox.removeChild(typingIndicator);
        displayMessage("I'm sorry, I encountered an error. Please try again later.", "bot-message");
    }
});

// Function to display messages in the chatbox
function displayMessage(message, className) {
    const chatbox = document.getElementById("chatbox");

    const messageContainer = document.createElement("div");
    messageContainer.className = className;

    const avatar = document.createElement("span");
    avatar.className = "avatar";

    if (className === "bot-message") {
        avatar.textContent = "🤖";
        messageContainer.appendChild(avatar);
    }

    const messageBubble = document.createElement("p");
    messageBubble.textContent = message;

    messageContainer.appendChild(messageBubble);
    chatbox.appendChild(messageContainer);

    // Scroll to the latest message
    chatbox.scrollTop = chatbox.scrollHeight;
}
