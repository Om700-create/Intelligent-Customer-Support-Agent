const chat = document.getElementById("chat");
const form = document.getElementById("form");
const input = document.getElementById("input");

function addMessage(text, who){
  const el = document.createElement("div");
  el.className = "msg " + (who === "user" ? "user" : "bot");
  el.textContent = text;
  chat.appendChild(el);
  chat.scrollTop = chat.scrollHeight;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if(!text) return;
  addMessage(text, "user");
  input.value = "";
  addMessage("...", "bot");
  const lastBot = chat.querySelectorAll(".bot");
  const loadingEl = lastBot[lastBot.length - 1];
  try{
    const resp = await fetch("/chat", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({message: text})
    });
    const data = await resp.json();
    if(data.reply){
      loadingEl.textContent = data.reply;
    } else {
      loadingEl.textContent = "Error: " + (data.error || "Unknown");
    }
  } catch(err){
    loadingEl.textContent = "Network error: " + err.message;
  }
});
