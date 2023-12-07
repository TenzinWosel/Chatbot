document.addEventListener('DOMContentLoaded', function () {
    const chatLog = document.getElementById('chat-log');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const botAvatarSrc = "/static/images/bot-avatar.png";
    const userAvatarSrc = "/static/images/user-avatar.png";

    sendButton.addEventListener('click', function (e) {
        e.preventDefault();
        sendMessage();
    });

    userInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });

    function sendMessage() {
        const userMessage = userInput.value.trim();
        if (userMessage === '') {
            return;
        }

        displayUserMessage(userMessage);
        userInput.value = '';

        // Send the user's message to the server (your Python code) using a fetch API call
        fetch('/api/healthcare-chatbot', {
            method: 'POST',
            body: JSON.stringify({ message: userMessage }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            displayBotMessage(data.response);
        })
        .catch(error => console.error('Error:', error));
    }

    function displayUserMessage(message) {
        const userMessageDiv = document.createElement('div');
        userMessageDiv.className = 'message user-message';
        userMessageDiv.innerHTML = `
            <div class="avatar user-avatar">
                <img src="${userAvatarSrc}" alt="User Avatar">
            </div>
            <div class="message-text">${message}</div>
        `;

        chatLog.appendChild(userMessageDiv);
        scrollToBottom();
    }

    function displayBotMessage(message) {
        const botMessageDiv = document.createElement('div');
        botMessageDiv.className = 'message bot-message';
        botMessageDiv.innerHTML = `
            <div class="avatar bot-avatar">
                <img src="${botAvatarSrc}" alt="Bot Avatar">
            </div>
            <div class "message-text">${message}</div>
        `;

        chatLog.appendChild(botMessageDiv);
        scrollToBottom();
    }

    function scrollToBottom() {
        chatLog.scrollTop = chatLog.scrollHeight;
    }
    
});

const logoutButton = document.getElementById('logout-button');

logoutButton.addEventListener('click', function () {
    // Redirect to the login page
    window.location.href = '/login';  // Update this URL if needed
});
