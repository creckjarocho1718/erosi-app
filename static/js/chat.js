// chat.js
window.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('chat-form');
  const input = document.getElementById('user-input');
  const chatWindow = document.getElementById('chat-window');
  const avatar = document.getElementById('erosi-avatar');

  function appendMessage(text, sender) {
    const div = document.createElement('div');
    div.classList.add('message', sender);
    div.textContent = text;
    chatWindow.appendChild(div);
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  form.addEventListener('submit', async e => {
    e.preventDefault();
    const userText = input.value.trim();
    if (!userText) return;
    appendMessage(userText, 'user');
    input.value = '';

    // Simula que Dr. Erosi "habla":
    avatar.style.animationName = 'speaking';

    // Simula retraso de respuesta
    setTimeout(() => {
      // Aquí llamarías a tu backend para obtener la respuesta real
      const erosiText = '¡Entiendo! Cuéntame más sobre eso…';
      appendMessage(erosiText, 'erosi');
      avatar.style.animationName = 'idle';
    }, 1000);
  });
});
