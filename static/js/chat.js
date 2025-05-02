window.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('chat-form');
  const input = document.getElementById('user-input');
  const chatWin = document.getElementById('chat-window');
  const avatar = document.getElementById('erosi-avatar');
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
    avatar.classList.replace('idle','speaking');

    try {
      const res = await fetch('/api/message',{
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({message:userText})
      });
      const data = await res.json();
      appendMessage(data.reply,'erosi');

      const ttsRes = await fetch('/api/tts?text='+encodeURIComponent(data.reply));
      const blob = await ttsRes.blob();
      const url = URL.createObjectURL(blob);
      const audio = new Audio(url);
      audio.play();
      audio.onended = ()=> avatar.classList.replace('speaking','idle');
    } catch(err){
      console.error(err);
      avatar.classList.replace('speaking','idle');
    }
  }

  form.addEventListener('submit', e => {
    e.preventDefault();
    const text = input.value.trim();
    if(!text) return;
    sendMessage(text);
  });
}/* end chat.js */