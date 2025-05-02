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

    avatar.style.animationName = 'speaking';

    const res = await fetch('/api/message', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: userText})
    });
    const data = await res.json();
    appendMessage(data.reply, 'erosi');

    const audioRes = await fetch('/api/tts?text=' + encodeURIComponent(data.reply));
    const audioBlob = await audioRes.blob();
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);
    audio.play();
    audio.onended = () => avatar.style.animationName = 'idle';
  });
});