import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

def client():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not configured on the server.")
    return OpenAI(api_key=key)

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/health")
def health():
    return {"ok": True, "service": "CUBAi"}

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify(error="Паём холӣ аст."), 400
    try:
        response = client().responses.create(
            model=os.getenv("OPENAI_CHAT_MODEL", "gpt-5"),
            instructions=(
                "Ту CUBAi ҳастӣ — ёвари AI барои корбарони тоҷик. "
                "Ба забони тоҷикӣ, равшан ва дӯстона ҷавоб деҳ. "
                "Агар корбар бо забони дигар нависад, ҳамон забонро истифода бар."
            ),
            input=message,
        )
        return jsonify(reply=response.output_text)
    except Exception as e:
        return jsonify(error=f"Хатои AI: {str(e)}"), 500

@app.post("/api/image")
def image():
    data = request.get_json(silent=True) or {}
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        return jsonify(error="Тавсифи тасвирро нависед."), 400
    try:
        result = client().images.generate(
            model=os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1"),
            prompt=prompt,
            size="1024x1024",
        )
        item = result.data[0]
        b64 = getattr(item, "b64_json", None)
        if not b64:
            return jsonify(error="AI тасвирро барнагардонд."), 500
        return jsonify(image=f"data:image/png;base64,{b64}")
    except Exception as e:
        return jsonify(error=f"Хатои render: {str(e)}"), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
