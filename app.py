import os
from flask import Flask, render_template, request, jsonify
from huggingface_hub import InferenceClient

app = Flask(__name__)

def client():
    token = os.getenv("HF_TOKEN")
    if not token:
        raise RuntimeError("HF_TOKEN is not configured on the server.")
    return InferenceClient(token=token)

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/health")
def health():
    return {"ok": True, "service": "CUBAi", "ai": "Hugging Face"}

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify(error="Паём холӣ аст."), 400
    try:
        result = client().chat.completions.create(
            model=os.getenv("HF_CHAT_MODEL", "Qwen/Qwen2.5-7B-Instruct"),
            messages=[
                {"role": "system", "content":
                 "Ту CUBAi ҳастӣ — ёвари AI барои корбарони тоҷик. "
                 "Ба забони тоҷикӣ, равшан ва дӯстона ҷавоб деҳ. "
                 "Агар корбар бо забони дигар нависад, ҳамон забонро истифода бар."},
                {"role": "user", "content": message}
            ],
            max_tokens=700,
        )
        return jsonify(reply=result.choices[0].message.content)
    except Exception as e:
        return jsonify(error=f"Хатои AI: {str(e)}"), 500

@app.post("/api/image")
def image():
    return jsonify(error="AI Render дар версияи ройгон ҳоло дастрас нест."), 503

if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
