window.addEventListener('DOMContentLoaded', () => {
  console.log("SCRIPT DEBUG: DOMContentLoaded");
  const form = document.getElementById('chat-form');
  const input = document.getElementById('user-input');
  const chatWin = document.getElementById('chat-window');
  const avatar = document.getElementById('erosi-avatar');
  console.log("SCRIPT DEBUG: avatar element:", avatar);

  function appendMessage(text, sender) {
    console.log("SCRIPT DEBUG: appendMessage:", sender, text);
    const div = document.createElement('div');
    div.classList.add('message', sender);
    div.textContent = text;
    chatWin.appendChild(div);
    chatWin.scrollTop = chatWin.scrollHeight;
  }

  async function sendMessage(userText) {
    console.log("SCRIPT DEBUG: sendMessage called with:", userText);
    appendMessage(userText, 'user');
    input.value = '';
    if (avatar) {
      console.log("SCRIPT DEBUG: switching to speaking animation");
      avatar.classList.replace('idle', 'speaking');
    }

    try {
      const msgRes = await fetch('/api/message', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: userText})
      });
      const msgData = await msgRes.json();
      console.log("SCRIPT DEBUG: msgData:", msgData);
      appendMessage(msgData.reply, 'erosi');

      const ttsRes = await fetch('/api/tts?text=' + encodeURIComponent(msgData.reply));
      const ttsBlob = await ttsRes.blob();
      const audioUrl = URL.createObjectURL(ttsBlob);
      const audio = new Audio(audioUrl);
      audio.play();
      audio.onended = () => {
        console.log("SCRIPT DEBUG: audio ended, back to idle");
        avatar.classList.replace('speaking', 'idle');
      };
    } catch(err) {
      console.error("SCRIPT DEBUG: error in sendMessage:", err);
    }
  }

  form.addEventListener('submit', e => {
    e.preventDefault();
    const text = input.value.trim();
    console.log("SCRIPT DEBUG: form submit with text:", text);
    if (!text) return;
    sendMessage(text);
  });
});
