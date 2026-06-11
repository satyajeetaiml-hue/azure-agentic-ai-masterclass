# Agentic AI on Azure — Enterprise Master Class (Starter Project)

[![CI](https://github.com/satyajeetaiml-hue/azure-agentic-ai-masterclass/actions/workflows/ci.yml/badge.svg)](https://github.com/satyajeetaiml-hue/azure-agentic-ai-masterclass/actions/workflows/ci.yml)

A production-oriented **FastAPI** starter for building agentic AI systems on Azure, structured to follow the
**12-Week Enterprise Master Class** (see [`docs/Course-Enterprise-UseCases.md`](docs/Course-Enterprise-UseCases.md)).

The project is designed so it **runs locally out of the box** (Week 1 "hello agent" works with a built-in mock
reasoning loop — no Azure keys required), and progressively layers in real Azure services week by week.

> Stack: **Python 3.11+ · FastAPI · Pydantic v2 · Uvicorn** · Microsoft Foundry · Microsoft Agent Framework ·
> MCP · A2A · Azure AI Search · Cosmos DB · Container Apps.

---

## Quick start

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy the env template (optional — app runs in MOCK mode without it)
copy .env.example .env        # Windows
# cp .env.example .env        # macOS/Linux

# 4. Run the API
uvicorn app.main:app --reload
```

Then open:

- Swagger UI: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health
- Week 1 hello-agent: `POST http://127.0.0.1:8000/api/v1/hello`

Example request:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/hello ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"My laptop won't connect to VPN and it's urgent\"}"
```

---

## Project layout

```
azure-agentic-ai-masterclass/
├── app/
│   ├── main.py            # FastAPI application + router registration
│   ├── config.py          # Pydantic settings (reads .env)
│   ├── core/
│   │   ├── agent_loop.py  # reason → plan → act → observe loop (mock + Azure-ready)
│   │   └── logging.py     # structured logging setup
│   ├── routers/
│   │   ├── hello.py       # Week 1 — IT Helpdesk Triage Agent
│   │   └── health.py      # liveness/readiness
│   └── schemas/
│       └── agent.py       # Pydantic request/response contracts
├── labs/                  # one folder per course week with its own README & TODOs
│   ├── week01_foundations/
│   ├── week02_foundry/
│   └── ...
├── docs/
│   └── Course-Enterprise-UseCases.md   # the full course companion
├── infra/                 # Bicep IaC placeholders (Container Apps, etc.)
├── tests/                 # pytest suite
├── .github/workflows/ci.yml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── pyproject.toml
```

---

## Running with Docker

```bash
docker build -t azure-agentic-ai .
docker run -p 8000:8000 azure-agentic-ai
```

Or with compose:

```bash
docker compose up --build
```

---

## Configuration

All settings live in `app/config.py` and are read from environment variables / `.env`.
See [`.env.example`](.env.example) for the full list. If `AZURE_OPENAI_ENDPOINT` is **not** set,
the agent loop falls back to a deterministic **mock** so the app stays runnable for learning.

| Variable | Purpose |
|----------|---------|
| `APP_ENV` | `local` / `dev` / `prod` |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI / Foundry endpoint (enables real model calls) |
| `AZURE_OPENAI_API_KEY` | Key (prefer Managed Identity in Azure) |
| `AZURE_OPENAI_DEPLOYMENT` | Chat model deployment name |

---

## The 12-week path

Each `labs/weekNN_*` folder maps to a week in the course companion and contains a `README.md`
with the learning goal, enterprise use case, and a hands-on TODO checklist. Start at
[`labs/week01_foundations`](labs/week01_foundations/README.md).

---

## Testing

```bash
pytest -q
```

---

## License

MIT — see [`LICENSE`](LICENSE).
