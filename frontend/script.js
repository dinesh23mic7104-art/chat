const BACKEND_URL = 'https://chat-8hnm.onrender.com/chat'; // ✅ Your Render backend URL

const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  appendMessage('You', message, 'user');
  userInput.value = '';
  appendMessage('Bot', 'Typing...', 'bot', true);

  try {
    const response = await fetch(BACKEND_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    removeTyping();
    appendMessage('Bot', data.reply, 'bot');
  } catch (error) {
    removeTyping();
    appendMessage('Bot', '⚠️ Connection error. Try again later.', 'bot');
  }
}

function appendMessage(sender, text, className, isTyping = false) {
  const msg = document.createElement('div');
  msg.classList.add('message', className);
  msg.textContent = isTyping ? text : ${sender}: ;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTyping() {
  const typingMessages = document.querySelectorAll('.message.bot');
  typingMessages.forEach(msg => {
    if (msg.textContent === 'Typing...') msg.remove();
  });
}

userInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') sendMessage();
});
