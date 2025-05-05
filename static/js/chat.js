let voz_activada = true;
document.getElementById("chat-form").addEventListener("submit", async function(e) {
    e.preventDefault();
    const input = document.getElementById("user-input");
    const message = input.value;
    input.value = "";
    const res = await fetch("/api/message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });
    const data = await res.json();
    document.getElementById("chat-window").innerHTML += "<p>" + data.text + "</p>";
    if (voz_activada && data.audio) {
        const audio = new Audio(data.audio);
        audio.play();
    }
});
