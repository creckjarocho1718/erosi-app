window.addEventListener('DOMContentLoaded', () => {
  const form      = document.getElementById('chat-form');
  const input     = document.getElementById('user-input');
  const chatWin   = document.getElementById('chat-window');
  const avatar    = document.getElementById('erosi-avatar');

  // Clase inicial de animación idle
  avatar.classList.add('idle');

  function appendMessage(text, sender) {
    const div = document.createElement('div');
    div.classList.add('message', sender);
    div.textContent = text;
    chatWin.appendChild(div);
    chatWin.scrollTop = chatWin.scrollHeight;
  }

  async function sendMessage(userText) {
    // Muestra tu mensaje
    appendMessage(userText, 'user');
    // Empieza animación de hablar
    avatar.classList.replace('idle', 'speaking');

    // ----- 1) ChatGPT -----
    const msgRes = await fetch('/api/message', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: userText})
    });
    const msgData = await msgRes.json();
    const erosiText = msgData.reply;
    appendMessage(erosiText, 'erosi');

    // ----- 2) Text‐to‐Speech -----
    const ttsRes = await fetch('/api/tts?text=' + encodeURIComponent(erosiText));
    const ttsBlob = await ttsRes.blob();
    const audioUrl = URL.createObjectURL(ttsBlob);
    const audio = new Audio(audioUrl);
    audio.play();
    // Cuando termine de hablar, vuelve a idle
    audio.onended = () => {
      avatar.classList.replace('speaking', 'idle');
    };
  }

  form.addEventListener('submit', e => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    input.value = '';
    sendMessage(text);
  });
});
