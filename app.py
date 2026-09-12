import os
from flask import Flask, render_template, request, jsonify
from huggingface_hub import InferenceClient

app = Flask(__name__)
DEFAULT_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"

def get_model():
    model = (os.getenv("HF_CHAT_MODEL") or DEFAULT_MODEL).strip()
    if "Qwen2.5-7B-Instruct-Turbo" in model:
        return DEFAULT_MODEL
    return model

def get_client():
    token = os.getenv("HF_TOKEN")
    if not token:
        raise RuntimeError("HF_TOKEN не настроен на сервере.")
    return InferenceClient(token=token)

SYSTEM_PROMPT = """Ты — CUBAi, умный ИИ-помощник.
Всегда отвечай ТОЛЬКО на русском языке.
Не используй таджикский, английский или другие языки, если пользователь прямо не попросил перевод.
Не смешивай языки и не придумывай бессмысленные слова.
Отвечай естественно, понятно и грамотно.
Если вопрос непонятен, попроси уточнить его на русском языке.
"""

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/health")
def health():
    return {"ok": True, "service": "CUBAi", "model": get_model()}

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify(error="Введите сообщение."), 400
    try:
        result = get_client().chat.completions.create(
            model=get_model(),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ],
            max_tokens=600,
            temperature=0.3
        )
        return jsonify(reply=result.choices[0].message.content.strip())
    except Exception as e:
        return jsonify(error=f"Ошибка ИИ: {str(e)}"), 500

@app.post("/api/image")
def image():
    return jsonify(error="Генерация изображений пока отключена в бесплатной версии."), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")))
