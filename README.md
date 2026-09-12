# CUBAi — Hugging Face fixed version

CUBAi is a Tajik-language AI chat website for Render.

## Render environment variables

Add:

- `HF_TOKEN` = your own Hugging Face Read token
- `HF_CHAT_MODEL` = `Qwen/Qwen2.5-1.5B-Instruct`

If an older Render variable contains `Qwen/Qwen2.5-7B-Instruct-Turbo`, this app automatically ignores that old value and uses the working default.

## Important

Do not put your HF token in GitHub or send it in chat.

This version focuses on text chat. AI image generation is intentionally disabled.

The Qwen 1.5B model is a smaller model and may be less capable than a 7B model, but it is much lighter for this setup.
