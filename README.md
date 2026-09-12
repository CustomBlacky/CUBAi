# CUBAi — AI бо интерфейси тоҷикӣ

CUBAi як веб-сайти AI мебошад: чат + генератори тасвир (AI Render).

## Локалӣ
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Дар муҳити худ `OPENAI_API_KEY`-ро ҳамчун secret гузоред, баъд:
```bash
gunicorn app:app
```

## Render
1. Репозиторийро ба GitHub гузоред.
2. Дар Render → New → Web Service → репозиторийро интихоб кунед.
3. Build: `pip install -r requirements.txt`
4. Start: `gunicorn app:app`
5. Environment Variable: `OPENAI_API_KEY`-ро илова кунед.
6. Deploy.

Номи service-ро `cubai` гузоред, то URL-и пешфарз `cubai.onrender.com` бошад, агар ин ном дар Render дастрас бошад.

**Муҳим:** API key-ро ба JavaScript ё GitHub commit накунед. Он танҳо дар Environment Variables-и Render нигоҳ дошта шавад.
