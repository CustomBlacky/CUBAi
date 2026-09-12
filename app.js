const form = document.getElementById("form");
const input = document.getElementById("input");
const chat = document.getElementById("chat");

function addMessage(text, who) {
  const box = document.createElement("div");
  box.className = "msg " + who;
  box.textContent = text;
  chat.appendChild(box);
  chat.scrollTop = chat.scrollHeight;
  return box;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  const welcome = document.querySelector(".welcome");
  if (welcome) welcome.remove();

  addMessage(message, "user");
  input.value = "";

  const thinking = addMessage("Фикр карда истодаам…", "ai");

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({message})
    });
    const data = await res.json();

    if (!res.ok) {
      thinking.textContent = data.error || "Хатои номаълум.";
    } else {
      thinking.textContent = data.reply || "Ҷавоб холӣ омад.";
    }
  } catch (err) {
    thinking.textContent = "Хатои пайвастшавӣ ба сервер.";
  }
});

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    form.requestSubmit();
  }
});
