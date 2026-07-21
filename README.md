
# 🪨 RockHe — GiMi 0.1

> API-first AI assistant for coding and general tasks.  
> Text-only. Markdown-native. Built to be extended.

---

## What is RockHe?

RockHe is a lightweight AI interface project. **GiMi 0.1** is the first release — a text-only API with a Markdown text box frontend, focused on clean output for both code and conversation.

---

## GiMi 0.1 Features

| Feature | Status |
|---|---|
| Text-only API | ✅ |
| Markdown rendering | ✅ |
| Code syntax highlighting | ✅ |
| General chat (`/chat`) | ✅ |
| Coding assistant (`/code`) | ✅ |

---

## Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/rockhe.git
cd rockhe
cp .env.example .env
# Edit .env with your API keys
./scripts/setup.sh
```

2. Start the API

```bash
./scripts/run.sh
# API runs at http://localhost:8000
```

3. Launch the UI

```bash
./scripts/serve-ui.sh
# Open http://localhost:3000
```

---

API Endpoints

`POST /chat`
General conversation.

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain recursion in simple terms"}'
```

`POST /code`
Coding-focused with optimized prompts.

```bash
curl -X POST http://localhost:8000/code \
  -H "Content-Type: application/json" \
  -d '{"message": "Write a Python function to flatten a nested list"}'
```

Response format:

```json
{
  "response": "Here's how you can do it...\n\n```python\ndef flatten(lst):\n    ...\n```",
  "tokens_used": 142,
  "model": "gimi-0.1"
}
```

---

Project Structure

```
RockHe/
├── src/          # Backend (FastAPI + GiMi engine)
├── ui/           # Frontend (Markdown text box)
├── tests/        # Unit tests
├── docs/         # Documentation
└── scripts/      # Dev helpers
```

---

Tech Stack

- Backend: Python, FastAPI
- Frontend: Vanilla JS, Markdown-it (or marked)
- Styling: Custom CSS
- AI: OpenAI API / local LLM (configurable)

---

Roadmap

- Streaming responses
- Conversation memory
- Multi-model support
- File upload (images, docs)
- GiMi 0.2 — tool use & plugins

---

License

MIT — see [LICENSE](LICENSE)

---

Built with 💻 by John Adman
