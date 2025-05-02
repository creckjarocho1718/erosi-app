window.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('chat-form');
  const input = document.getElementById('user-input');
  const chatWin = document.getElementById('chat-window');
  const avatar = document.getElementById('erosi-avatar');

  // Inicializa animación idle
  avatar.classList.add('idle');

  function appendMessage(text, sender) {
    const div = document.createElement('div');
    div.classList.add('message', sender);
    div.textContent = text;
    chatWin.appendChild(div);
    chatWin.scrollTop = chatWin.scrollHeight;
  }

  async function sendMessage(userText) {
    appendMessage(userText, 'user');
    input.value = '';

    // Avatar habla
    avatar.classList.replace('idle', 'speaking');

    // 1) Obtener respuesta de ChatGPT
    const msgRes = await fetch('/api/message', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: userText})
    });
    const msgData = await msgRes.json();
    const erosiText = msgData.reply;
    appendMessage(erosiText, 'erosi');

    // 2) Text-to-Speech
    const ttsRes = await fetch('/api/tts?text=' + encodeURIComponent(erosiText));
    const ttsBlob = await ttsRes.blob();
    const audioUrl = URL.createObjectURL(ttsBlob);
    const audio = new Audio(audioUrl);
    audio.play();
    audio.onended = () => {
      avatar.classList.replace('speaking', 'idle');
    };
  }

  form.addEventListener('submit', e => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    sendMessage(text);
  });
});
