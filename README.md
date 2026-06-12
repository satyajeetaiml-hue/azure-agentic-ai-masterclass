# Agentic AI on Azure — Enterprise Master Class (Starter Project)

[![CI](https://github.com/satyajeetaiml-hue/azure-agentic-ai-masterclass/actions/workflows/ci.yml/badge.svg)](https://github.com/satyajeetaiml-hue/azure-agentic-ai-masterclass/actions/workflows/ci.yml)

A production-oriented **FastAPI** starter for building agentic AI systems on Azure, structured to follow the
**12-Week Enterprise Master Class** (see [`docs/Course-Enterprise-UseCases.md`](docs/Course-Enterprise-UseCases.md)).

The project is designed so it **runs locally out of the box** (Week 1 "hello agent" works with a built-in mock
reasoning loop — no Azure keys required), and progressively layers in real Azure services week by week.

> Stack: **Python 3.11+ · FastAPI · Pydantic v2 · Uvicorn** · Microsoft Foundry · Microsoft Agent Framework ·
> MCP · A2A · Azure AI Search · Cosmos DB · Container Apps.

---

## 🏗️ Architecture

The "north star" you build toward across the 12 weeks. Each block is annotated with the week(s) that
implement it. (A plain-text version is in [`docs/Course-Enterprise-UseCases.md`](docs/Course-Enterprise-UseCases.md).)

```mermaid
flowchart TB
    C["Clients / Channels<br/>Web · Teams · API consumers · M365 Copilot"]
    C -->|"HTTPS / OAuth2 (Entra ID)"| GW["API Management<br/>rate limiting · JWT validation · WAF"]
    GW --> API

    subgraph API["FastAPI Orchestration Layer — the spine of every lab"]
        direction TB
        EP["/triage · /claims · /research · /procure · /underwrite<br/>/policy · /support · /advise · /hr · /capstone<br/>async · SSE streaming · Pydantic contracts"]
    end

    API --> FA["Foundry Agent Service<br/>(Wk 1–2)"]
    API --> AF["Agent Framework<br/>memory · middleware (Wk 3–4)"]
    API --> MCP["MCP / Tools Hub<br/>(Wk 5)"]
    API --> ORCH["Multi-Agent Orchestration<br/>concurrent · handoff · HITL (Wk 6–7)"]

    FA --> GROUND
    AF --> GROUND
    MCP --> GROUND
    ORCH --> GROUND

    subgraph GROUND["Grounding & State"]
        direction LR
        AIS["Azure AI Search<br/>RAG + security trimming (Wk 8)"]
        COS["Cosmos DB<br/>memory / run state"]
        RED["Redis<br/>session cache"]
        BLOB["Blob Storage"]
    end

    subgraph CROSS["Cross-cutting concerns"]
        direction LR
        IDN["Identity & Security<br/>Entra ID · Managed Identity · Key Vault · OBO (Wk 11)"]
        OBS["Observability & Quality<br/>OpenTelemetry · App Insights · Evaluations (Wk 10)"]
    end

    API -.-> CROSS
    GROUND --> DEPLOY

    subgraph DEPLOY["Deployment substrate (Wk 9)"]
        SUB["Azure Container Apps · AKS · Functions<br/>Docker · Bicep/Terraform · GitHub Actions CI/CD"]
    end
```

---

## 📚 Lab index — one repo per week

This repo is the **course hub**. Each week is also published as a **standalone, runnable repo**.

> ✅ **All 12 weeks are fully built out** — every lab ships a runnable offline **mock backend**
> (deterministic, fully tested) plus a lazy-imported **real Azure backend** selected by env vars, with
> typed schemas, hermetic tests, a detailed README, Dockerfile, and green CI. **61 tests passing across
> all repos.** Clone any week and run `uvicorn app.main:app --reload`.

| Week | Lab repo | Enterprise use case | Key built-out feature | Status |
|------|----------|---------------------|-----------------------|:------:|
| **1** | [week01-foundations](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week01-foundations) | IT Helpdesk Triage Agent | reason→plan→act→observe loop + Foundry Responses | ✅ Built out |
| **2** | [week02-foundry-claims](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week02-foundry-claims) | Insurance Claims Intake | Foundry Agent Service **function tool** loop | ✅ Built out |
| **3–4** | [week03-04-agent-framework](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week03-04-agent-framework) | Wealth Research Assistant | memory + middleware (PII/disclaimer) + tools | ✅ Built out |
| **5** | [week05-mcp-tools](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week05-mcp-tools) | Procurement Operations Agent | tool registry + idempotency + MCP discovery | ✅ Built out |
| **6–7** | [week06-07-multi-agent](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week06-07-multi-agent) | Loan Underwriting Pipeline | concurrent agents + human-in-the-loop resume | ✅ Built out |
| **8** | [week08-rag-grounding](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week08-rag-grounding) | Clinical Policy Assistant (RAG) | retrieval + security trimming + citations | ✅ Built out |
| **9** | [week09-hosting-scale](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week09-hosting-scale) | Customer Service Swarm | durable background tasks + status polling | ✅ Built out |
| **10** | [week10-observability](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week10-observability) | Advice Quality Monitoring | eval scoring + metrics/traces + OTel | ✅ Built out |
| **11** | [week11-security](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week11-security) | HR Self-Service (least privilege) | Entra JWT + OBO + RBAC + audit | ✅ Built out |
| **12** | [week12-capstone](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week12-capstone) | Capstone onboarding pipeline | staged multi-agent pipeline | ✅ Built out |

Each lab endpoint is listed in its own README. Backends run in **mock mode** with no Azure; set the
documented env vars (+ `az login`) to switch to the real Azure backend.

> Browse them all: **https://github.com/satyajeetaiml-hue?tab=repositories&q=agentic-ai-azure**

---

## 🧪 Other agent frameworks (bonus projects)

The labs use the **Microsoft Agent Framework / Foundry**. These companion repos solve the same kind of
problem with the two other major frameworks, so you can compare APIs side by side. Both run **for real
offline** (the framework executes; Azure OpenAI is optional) and have green CI.

| Framework | Repo | What it shows |
|-----------|------|---------------|
| **LangGraph** | [agentic-ai-azure-langgraph](https://github.com/satyajeetaiml-hue/agentic-ai-azure-langgraph) | A `StateGraph` triage agent — nodes + conditional edges + state; optional Azure OpenAI node |
| **Semantic Kernel** | [agentic-ai-azure-semantic-kernel](https://github.com/satyajeetaiml-hue/agentic-ai-azure-semantic-kernel) | A `Kernel` + native plugin (`@kernel_function`); optional Azure automatic function calling |

📖 **[COMPARISON.md](COMPARISON.md)** — Microsoft Agent Framework vs. LangGraph vs. Semantic Kernel:
abstractions, control flow, state, tools, Azure fit, the same agent in each, and how to choose.

### Semantic Kernel + Azure data services
Focused Semantic Kernel projects pairing a real SK kernel + native plugin with one Azure data store
(each runs offline with an in-memory store; the Azure service is the optional backend):

| Azure service | Repo | Use case |
|---------------|------|----------|
| **Azure Database for PostgreSQL** | [agentic-ai-azure-sk-postgresql](https://github.com/satyajeetaiml-hue/agentic-ai-azure-sk-postgresql) | Orders Assistant — plugin queries a relational `orders` table |
| **Azure AI Search** | [agentic-ai-azure-sk-ai-search](https://github.com/satyajeetaiml-hue/agentic-ai-azure-sk-ai-search) | Knowledge Assistant (RAG) — plugin retrieves + cites sources |
| **Azure Cosmos DB** | [agentic-ai-azure-sk-cosmosdb](https://github.com/satyajeetaiml-hue/agentic-ai-azure-sk-cosmosdb) | Durable conversation memory — plugin remembers/recalls turns |

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

## 📖 Course book (PDF)

A single **75-page printable book** compiling the whole project — cover, table of contents, and a
chapter per repo (README + key source code), organized into parts (Overview · Weekly Labs · Framework
Comparison · SK + Azure Data Services). Great as a teaching handout.

**Download:** [`docs/Agentic-AI-on-Azure-Course-Book.pdf`](docs/Agentic-AI-on-Azure-Course-Book.pdf)

---

## 📊 Teaching slides

Every repo ships a **7-slide deck** (`.pptx`, with presenter notes) and a **PDF handout** (slides + notes).
This is the master index — links download the file directly.

> Slides per deck: Title · Learning goal · Enterprise use case · Architecture/flow · Key concepts · Run it · Architect's takeaways.

**This hub:** [Deck](slides/azure-agentic-ai-masterclass.pptx) · [Handout (PDF)](slides/azure-agentic-ai-masterclass-handout.pdf)

### Weekly labs
| Week | Download |
|------|----------|
| 1 — Foundations | [Deck](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week01-foundations/raw/main/slides/agentic-ai-azure-week01-foundations.pptx) · [PDF](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week01-foundations/raw/main/slides/agentic-ai-azure-week01-foundations-handout.pdf) |
| 2 — Foundry Claims | [Deck](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week02-foundry-claims/raw/main/slides/agentic-ai-azure-week02-foundry-claims.pptx) · [PDF](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week02-foundry-claims/raw/main/slides/agentic-ai-azure-week02-foundry-claims-handout.pdf) |
| 3–4 — Agent Framework | [Deck](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week03-04-agent-framework/raw/main/slides/agentic-ai-azure-week03-04-agent-framework.pptx) · [PDF](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week03-04-agent-framework/raw/main/slides/agentic-ai-azure-week03-04-agent-framework-handout.pdf) |
| 5 — MCP & Tools | [Deck](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week05-mcp-tools/raw/main/slides/agentic-ai-azure-week05-mcp-tools.pptx) · [PDF](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week05-mcp-tools/raw/main/slides/agentic-ai-azure-week05-mcp-tools-handout.pdf) |
| 6–7 — Multi-Agent | [Deck](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week06-07-multi-agent/raw/main/slides/agentic-ai-azure-week06-07-multi-agent.pptx) · [PDF](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week06-07-multi-agent/raw/main/slides/agentic-ai-azure-week06-07-multi-agent-handout.pdf) |
| 8 — RAG | [Deck](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week08-rag-grounding/raw/main/slides/agentic-ai-azure-week08-rag-grounding.pptx) · [PDF](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week08-rag-grounding/raw/main/slides/agentic-ai-azure-week08-rag-grounding-handout.pdf) |
| 9 — Hosting & Scale | [Deck](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week09-hosting-scale/raw/main/slides/agentic-ai-azure-week09-hosting-scale.pptx) · [PDF](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week09-hosting-scale/raw/main/slides/agentic-ai-azure-week09-hosting-scale-handout.pdf) |
| 10 — Observability | [Deck](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week10-observability/raw/main/slides/agentic-ai-azure-week10-observability.pptx) · [PDF](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week10-observability/raw/main/slides/agentic-ai-azure-week10-observability-handout.pdf) |
| 11 — Security | [Deck](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week11-security/raw/main/slides/agentic-ai-azure-week11-security.pptx) · [PDF](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week11-security/raw/main/slides/agentic-ai-azure-week11-security-handout.pdf) |
| 12 — Capstone | [Deck](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week12-capstone/raw/main/slides/agentic-ai-azure-week12-capstone.pptx) · [PDF](https://github.com/satyajeetaiml-hue/agentic-ai-azure-week12-capstone/raw/main/slides/agentic-ai-azure-week12-capstone-handout.pdf) |

### Framework comparison projects
| Project | Download |
|---------|----------|
| LangGraph | [Deck](https://github.com/satyajeetaiml-hue/agentic-ai-azure-langgraph/raw/main/slides/agentic-ai-azure-langgraph.pptx) · [PDF](https://github.com/satyajeetaiml-hue/agentic-ai-azure-langgraph/raw/main/slides/agentic-ai-azure-langgraph-handout.pdf) |
| Semantic Kernel | [Deck](https://github.com/satyajeetaiml-hue/agentic-ai-azure-semantic-kernel/raw/main/slides/agentic-ai-azure-semantic-kernel.pptx) · [PDF](https://github.com/satyajeetaiml-hue/agentic-ai-azure-semantic-kernel/raw/main/slides/agentic-ai-azure-semantic-kernel-handout.pdf) |

### Semantic Kernel + Azure data services
| Project | Download |
|---------|----------|
| SK + PostgreSQL | [Deck](https://github.com/satyajeetaiml-hue/agentic-ai-azure-sk-postgresql/raw/main/slides/agentic-ai-azure-sk-postgresql.pptx) · [PDF](https://github.com/satyajeetaiml-hue/agentic-ai-azure-sk-postgresql/raw/main/slides/agentic-ai-azure-sk-postgresql-handout.pdf) |
| SK + AI Search | [Deck](https://github.com/satyajeetaiml-hue/agentic-ai-azure-sk-ai-search/raw/main/slides/agentic-ai-azure-sk-ai-search.pptx) · [PDF](https://github.com/satyajeetaiml-hue/agentic-ai-azure-sk-ai-search/raw/main/slides/agentic-ai-azure-sk-ai-search-handout.pdf) |
| SK + Cosmos DB | [Deck](https://github.com/satyajeetaiml-hue/agentic-ai-azure-sk-cosmosdb/raw/main/slides/agentic-ai-azure-sk-cosmosdb.pptx) · [PDF](https://github.com/satyajeetaiml-hue/agentic-ai-azure-sk-cosmosdb/raw/main/slides/agentic-ai-azure-sk-cosmosdb-handout.pdf) |

