const voiceToggle = document.getElementById("voiceToggle");

function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value.trim();
    if (!message) return;
    appendMessage(message, "user");
    input.value = "";
    fetch("/chat/message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    })
    .then(res => res.json())
    .then(data => {
        appendMessage(data.response, "erosi");
        if (voiceToggle.checked) speak(data.response);
    });
}

function appendMessage(text, sender) {
    const chat = document.getElementById("chat");
    const div = document.createElement("div");
    div.className = 'message ' + sender;
    div.textContent = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function speak(text) {
    const utt = new SpeechSynthesisUtterance(text);
    utt.lang = "es-ES";
    speechSynthesis.speak(utt);
}



function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('open');
}
