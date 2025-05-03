window.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('chat-form');
  const input = document.getElementById('user-input');
  const chatWin = document.getElementById('chat-window');
  const avatarVideo = document.getElementById('erosi-avatar');
  const avatarImg = document.getElementById('erosi-img');

  // Initially show image, hide video
  avatarImg.style.display = 'block';
  avatarVideo.style.display = 'none';

  // When video can play, show video and hide image
  avatarVideo.addEventListener('canplay', () => {
    avatarImg.style.display = 'none';
    avatarVideo.style.display = 'block';
    avatarVideo.classList.add('idle');
  });

  // On error, keep image
  avatarVideo.onerror = () => {
    avatarVideo.style.display = 'none';
    avatarImg.style.display = 'block';
  };

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
    // Trigger speaking animation on video or do nothing on image
    if (avatarVideo.style.display !== 'none') {
      avatarVideo.classList.replace('idle', 'speaking');
    }

    try {
      const res = await fetch('/api/message',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({message:userText})
      });
      const data = await res.json();
      appendMessage(data.reply,'erosi');

      const ttsRes = await fetch('/api/tts?text=' + encodeURIComponent(data.reply));
      const blob = await ttsRes.blob();
      const url = URL.createObjectURL(blob);
      const audio = new Audio(url);
      audio.play();
      audio.onended = () => {
        if (avatarVideo.style.display !== 'none') {
          avatarVideo.classList.replace('speaking', 'idle');
        }
      };
    } catch(err){
      console.error(err);
      if (avatarVideo.style.display !== 'none') {
        avatarVideo.classList.replace('speaking', 'idle');
      }
    }
  }

  form.addEventListener('submit', e => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    sendMessage(text);
  });
});

/* Note: Ensure CSS defines .idle and .speaking animations */
