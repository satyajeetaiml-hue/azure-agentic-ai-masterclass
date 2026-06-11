# Agentic AI on Azure — Enterprise Use Cases & Architect's Companion

> **Instructor companion** for the 12-Week Master Class. Maps every week to **practical labs**, **enterprise use cases**, the **Azure AI Architect decision lens**, and the **full FastAPI + deployment tech stack**.
> Audience: AI Engineers, Solution Architects, Backend/Platform Engineers, Data/ML teams.
> Stack: **Python + .NET (C#)** · Microsoft Foundry · Microsoft Agent Framework 1.0 · FastAPI · MCP · A2A · OpenAPI

---

## How to Read This Document
Each week contains:
- **🎯 Learning goal** — the capability acquired
- **🏢 Enterprise use case** — a realistic, regulated-industry scenario
- **🧪 Practical lab** — what students build hands-on
- **🏗️ Architect's lens** — trade-offs, non-functional requirements, design decisions
- **🧰 Tech stack** — Azure services + libraries used that week

---

## Reference Architecture (the "north star" you build toward)

```
                          ┌──────────────────────────────────────────────┐
                          │              Client / Channels                │
                          │  Web · Teams · API consumers · M365 Copilot   │
                          └───────────────────────┬──────────────────────┘
                                                  │ HTTPS / OAuth2 (Entra ID)
                          ┌───────────────────────▼──────────────────────┐
                          │      API Gateway  (Azure API Management)       │
                          │   Rate limiting · JWT validation · WAF         │
                          └───────────────────────┬──────────────────────┘
                                                  │
                          ┌───────────────────────▼──────────────────────┐
                          │        FastAPI Orchestration Layer             │
                          │  /chat /agents /tools · SSE streaming · async  │
                          │  Pydantic contracts · OpenTelemetry traces     │
                          └───┬───────────────┬───────────────┬──────────┘
                              │               │               │
                ┌─────────────▼──┐   ┌────────▼────────┐  ┌───▼─────────────┐
                │ Foundry Agent  │   │ Microsoft Agent │  │  MCP Tool Hub   │
                │   Service      │   │  Framework 1.0  │  │ (Functions/Logic│
                │ (hosted agents)│   │ (orchestration) │  │  Apps/REST/DB)  │
                └───────┬────────┘   └────────┬────────┘  └───┬─────────────┘
                        │                     │               │
        ┌───────────────▼─────────────────────▼───────────────▼──────────────┐
        │                       Grounding & State                            │
        │  Azure AI Search (RAG) · Cosmos DB (memory) · Azure SQL · Blob     │
        │  Azure Cache for Redis (session) · ACL/permission trimming         │
        └────────────────────────────────────┬───────────────────────────────┘
                                              │
        ┌─────────────────────────────────────▼──────────────────────────────┐
        │            Cross-cutting: Identity · Observability · Governance     │
        │  Entra ID · Managed Identity · Key Vault · App Insights ·           │
        │  Azure Monitor · Content Safety · Foundry Evaluations · Purview     │
        └─────────────────────────────────────────────────────────────────────┘

   Deployment substrate:  Azure Container Apps  /  AKS  /  Azure Functions
   Packaged with: Docker · Bicep/Terraform · GitHub Actions / Azure DevOps
```

---

# Week-by-Week: Use Cases, Labs & Architecture

## Week 1 — Foundations of Agentic AI
**🎯 Goal:** Understand agent loops (reason → plan → act → observe), tool use, and where each Azure service fits.

**🏢 Enterprise use case — "IT Helpdesk Triage Agent" (Cross-industry)**
A single agent that reads an incoming support ticket, reasons about category/severity, and either answers from a knowledge base or escalates. Establishes the mental model before adding complexity.

**🧪 Lab:** Build a "hello agent" with a reasoning loop + one tool (ticket-lookup mock). Run locally, then deploy a `/hello` FastAPI endpoint.

**🏗️ Architect's lens:**
- When is an *agent* the right pattern vs. a deterministic workflow or a single LLM call? (Cost, latency, auditability.)
- Map the Azure agentic landscape: Foundry vs. Agent Framework vs. raw model calls.
- Define your "agent contract": inputs, tools, guardrails, success criteria.

**🧰 Tech stack:** Python 3.11+, FastAPI, Pydantic, Microsoft Foundry project, Azure OpenAI/Foundry models, `uvicorn`.

---

## Week 2 — Microsoft Foundry & Foundry Agent Service
**🎯 Goal:** Create hosted agents in Foundry Agent Service; expose them via FastAPI.

**🏢 Enterprise use case — "Insurance Claims Intake Agent" (Insurance)**
Customer submits a claim; the agent extracts structured fields, validates policy number, checks coverage, and creates a case. Uses Foundry-hosted agent with a tool to call the policy system.

**🧪 Lab:** Provision a Foundry project + Agent Service agent. Add a tool (policy-lookup), test in the playground, then wrap the agent behind a FastAPI `/claims/intake` endpoint exposing the agent as a REST API.

**🏗️ Architect's lens:**
- Hosted agents (managed runtime, threads, tool calls) vs. self-orchestrated. When does the managed thread/state model save you ops effort?
- Quota, model routing, and region selection for data residency.
- Securing the Foundry connection from FastAPI with **Managed Identity** (no keys in code).

**🧰 Tech stack:** Foundry Agent Service, Azure AI Foundry SDK, FastAPI, Azure Managed Identity, Key Vault, Pydantic models for claim schema.

---

## Weeks 3–4 — Microsoft Agent Framework (AutoGen + Semantic Kernel unified)
**🎯 Goal:** Use Agent Framework for memory, connectors, middleware, multi-channel deploy, and YAML-defined orchestration.

**🏢 Enterprise use case — "Wealth Management Research Assistant" (Financial Services)**
An advisor asks for a portfolio summary. A grounded agent pulls holdings (tool), market data (tool), applies compliance disclaimers (middleware), and streams a narrative back. Memory keeps the advisor's context across the session.

**🧪 Lab:**
- Build the agent with short-term + persistent memory (Cosmos DB).
- Add **middleware** for input/output filtering (PII redaction, disclaimer injection).
- Define the agent + workflow in **YAML**, stream responses via FastAPI **SSE**.

**🏗️ Architect's lens:**
- Memory tiers: session (Redis) vs. durable (Cosmos DB) vs. semantic (AI Search). Cost & consistency trade-offs.
- Middleware as a governance seam — where to enforce policy without touching agent logic.
- Declarative (YAML) vs. code-first definitions for versioning and CI/CD.

**🧰 Tech stack:** Microsoft Agent Framework 1.0, Semantic Kernel concepts, Azure Cosmos DB, Azure Cache for Redis, FastAPI (SSE/StreamingResponse), Azure Content Safety for filtering.

---

## Week 5 — Tools, MCP & Interoperability
**🎯 Goal:** Connect agents to tools via REST APIs, OpenAPI, Functions, Logic Apps, and a custom **MCP server**.

**🏢 Enterprise use case — "Procurement Operations Agent" (Manufacturing/Retail)**
The agent checks inventory (REST), creates a purchase order (Logic App), gets supplier pricing (OpenAPI tool), and logs to the ERP — all via standardized tool contracts so tools are reusable across agents.

**🧪 Lab:**
- Register an **OpenAPI** tool and an **Azure Function** tool.
- Build a **custom MCP server** exposing internal APIs as MCP tools.
- Front the MCP server / tools with FastAPI + **API Management** as the secure gateway.

**🏗️ Architect's lens:**
- MCP as the *interoperability contract* — decouple tools from agents so they're portable (the MCP/A2A/OpenAPI standards highlighted on the course).
- Tool governance: who can call what, schemas as the trust boundary, idempotency for write tools.
- Gateway pattern: rate limits, auth, and observability centralized at APIM.

**🧰 Tech stack:** MCP (Model Context Protocol) server, OpenAPI, Azure Functions, Azure Logic Apps, Azure API Management, FastAPI, Pydantic tool schemas.

---

## Weeks 6–7 — Multi-Agent Orchestration Patterns
**🎯 Goal:** Implement sequential, concurrent, handoff, group-chat, and graph-based orchestration with human-in-the-loop.

**🏢 Enterprise use case — "Loan Underwriting Pipeline" (Banking)**
- **Intake Agent** → extracts application data
- **Credit Risk Agent** (concurrent) → pulls credit + computes risk
- **Compliance Agent** (concurrent) → KYC/AML checks
- **Underwriter Agent** (handoff) → decision, with **human-in-the-loop** approval for edge cases
- Orchestrated as a graph; results aggregated and explained.

**🧪 Lab:** Build the multi-agent graph using Agent Framework orchestration. Implement an approval **pause/resume** with Durable Tasks. Expose `/underwrite` via FastAPI with async background execution + status polling.

**🏗️ Architect's lens:**
- Pattern selection: when concurrency helps (independent sub-tasks) vs. sequential dependencies.
- Human-in-the-loop checkpoints and durable state for long-running approvals.
- Inter-agent communication via **A2A** + event-driven topologies (Service Bus / Event Grid).
- Failure handling: partial results, compensation, retries.

**🧰 Tech stack:** Microsoft Agent Framework orchestration, A2A protocol, Azure Service Bus / Event Grid, Azure Durable Functions / Durable Tasks, FastAPI BackgroundTasks, Cosmos DB for run state.

---

## Week 8 — Memory, State & Grounding (RAG)
**🎯 Goal:** Build retrieval-grounded agents with permission-aware knowledge over enterprise data.

**🏢 Enterprise use case — "Clinical Policy Assistant" (Healthcare)**
Clinicians query care protocols. The agent retrieves from a curated knowledge base in Azure AI Search, **trims results by the user's role/department (security trimming)**, cites sources, and never answers beyond grounded content.

**🧪 Lab:**
- Ingest documents → chunk → embed → index in **Azure AI Search** (vector + hybrid + semantic ranker).
- Implement **permission/ACL trimming** using Entra group claims.
- RAG endpoint in FastAPI with citation payloads.

**🏗️ Architect's lens:**
- Retrieval quality: chunking strategy, hybrid search, reranking, recency.
- Security trimming as a first-class requirement (PHI/PII — never leak across boundaries).
- Grounding vs. hallucination guardrails; "I don't know" behavior.
- State backends: short-term threads vs. long-term knowledge.

**🧰 Tech stack:** Azure AI Search (vector/hybrid/semantic), Azure OpenAI embeddings, Azure Blob Storage, Cosmos DB, Entra ID groups for ACL, FastAPI.

---

## Week 9 — Hosting, Deployment & Scale
**🎯 Goal:** Package and deploy agents for production scale on Azure compute substrates.

**🏢 Enterprise use case — "Black-Friday Customer Service Swarm" (Retail/E-commerce)**
A fleet of customer-service agents must scale from 10 to 10,000 concurrent sessions, scale to zero overnight, and stay within cost guardrails — with durable long-running tasks for refunds.

**🧪 Lab:**
- Containerize the FastAPI agent app with **Docker**.
- Deploy to **Azure Container Apps** with autoscaling (KEDA, scale-to-zero).
- Add **Durable Tasks** for long-running operations.
- Compare deploy targets: Container Apps vs. **AKS** vs. **Azure Functions**.

**🏗️ Architect's lens:**
- **Decision matrix** (see appendix): Container Apps (managed, event-driven, scale-to-zero) vs. AKS (max control, multi-team, service mesh) vs. Functions (bursty, short tasks).
- Concurrency model: async FastAPI + `uvicorn`/`gunicorn` workers; connection pooling to models.
- Cost: token budgets, model routing (small model for triage, large for hard cases), caching.

**🧰 Tech stack:** Docker, Azure Container Apps (+ KEDA), AKS, Azure Functions, Azure Container Registry, FastAPI + Gunicorn/Uvicorn, Bicep/Terraform.

---

## Week 10 — Observability, Evaluation & Governance
**🎯 Goal:** Trace, evaluate, and continuously improve agents in production.

**🏢 Enterprise use case — "Regulated Advice Quality Monitoring" (Financial Services)**
Every agent interaction is traced end-to-end, scored for groundedness/relevance/safety, and flagged when quality drops — feeding a quality dashboard auditors can review.

**🧪 Lab:**
- Instrument FastAPI + agents with **OpenTelemetry** → Application Insights.
- Run **Foundry Evaluations** (groundedness, relevance, coherence, safety) offline + online.
- Build a quality dashboard; set alerts on metric thresholds.

**🏗️ Architect's lens:**
- Distributed tracing across agent hops and tool calls (trace/span per agent).
- Offline eval (regression gates in CI) vs. online eval (production sampling).
- Golden datasets, A/B prompts, drift detection.
- Cost & latency observability per token / per tool.

**🧰 Tech stack:** OpenTelemetry, Azure Application Insights, Azure Monitor, Foundry Evaluation SDK, Azure Content Safety, FastAPI middleware for tracing.

---

## Week 11 — Enterprise Security & Compliance
**🎯 Goal:** Secure agents with identity, RBAC, OAuth2/OBO, secrets, and compliance guardrails.

**🏢 Enterprise use case — "HR Self-Service Agent with Least Privilege" (Enterprise/Public Sector)**
Employees ask about benefits/payroll. The agent acts **on behalf of** the signed-in user (OBO flow), so it only sees data that user is entitled to. All secrets in Key Vault; all calls audited.

**🧪 Lab:**
- Protect FastAPI with **Microsoft Entra ID** (JWT validation, scopes/roles).
- Implement **OAuth2 On-Behalf-Of** so tools run with user identity.
- Move all secrets to **Key Vault** + **Managed Identity**; add input/output compliance filters.

**🏗️ Architect's lens:**
- Identity boundaries: app identity vs. user identity vs. tool identity.
- Data exfiltration & prompt-injection defenses (tool allow-lists, output filtering).
- RBAC + Conditional Access; private networking (Private Endpoints, VNet integration).
- Audit/compliance: who did what, retention, **Microsoft Purview** lineage.

**🧰 Tech stack:** Microsoft Entra ID, OAuth2/OBO, MSAL, Azure Key Vault, Managed Identity, Private Endpoints/VNet, Azure Content Safety, Microsoft Purview.

---

## Week 12 — Capstone: Build, Demo & Review
**🎯 Goal:** Ship a production-ready, multi-agent application end-to-end on Azure.

**🏢 Capstone scenarios (pick one):**
| Scenario | Industry | Key agents |
|----------|----------|-----------|
| Customer Onboarding Automation | Banking/Telecom | Intake · KYC · Risk · Provisioning |
| Financial Transaction Compliance | FinTech | Monitor · Rules · Investigation · Report |
| Supply-Chain / Sales-Lead Prioritization | Manufacturing/B2B | Enrichment · Scoring · Routing |
| Document Generation Workflow | Legal/Insurance | Retrieve · Draft · Review · Approve |

**🧪 Deliverables:**
- Multi-agent app (2–4 coordinating agents) with tools via MCP/OpenAPI.
- Grounding on enterprise data with permission-aware retrieval.
- FastAPI service, containerized, deployed to Container Apps/AKS with CI/CD.
- Identity, observability, evaluation, and guardrails wired in.
- Architecture write-up + live demo.

**🏗️ Architect's lens:** Defend your design — pattern choice, deployment target, cost model, security posture, and how you'd operate it on day-2.

---

# Appendix A — Full Tech Stack Reference

### Application / Agent Layer
| Concern | Technology |
|---------|-----------|
| Language | Python 3.11+, .NET 8 (C#) |
| Agent runtime | Microsoft Foundry Agent Service, Microsoft Agent Framework 1.0 |
| Models | Azure AI Foundry / Azure OpenAI (GPT-class), small models for triage |
| Tools/Interop | **MCP**, **A2A**, **OpenAPI**, Azure Functions, Logic Apps |
| API framework | **FastAPI** (async, SSE/WebSocket streaming, Pydantic v2) |
| ASGI server | Uvicorn + Gunicorn workers |
| Validation/contracts | Pydantic, JSON Schema |

### Data / Grounding / State
| Concern | Technology |
|---------|-----------|
| Vector/Hybrid search (RAG) | Azure AI Search (vector + semantic ranker) |
| Memory / run state | Azure Cosmos DB |
| Session cache | Azure Cache for Redis |
| Relational | Azure SQL Database |
| Files/blobs | Azure Blob Storage |
| Embeddings | Azure OpenAI embedding models |

### Security & Identity
Microsoft Entra ID · OAuth2 / On-Behalf-Of · MSAL · Managed Identity · Azure Key Vault · Private Endpoints / VNet · Azure Content Safety · Microsoft Purview · Azure API Management (auth gateway, WAF).

### Observability & Quality
OpenTelemetry · Azure Application Insights · Azure Monitor / Log Analytics · Foundry Evaluations (groundedness, relevance, safety) · Azure Content Safety.

### Deployment & DevOps (full chain)
| Stage | Technology |
|-------|-----------|
| Containerization | Docker |
| Registry | Azure Container Registry (ACR) |
| Compute (managed) | **Azure Container Apps** (KEDA autoscale, scale-to-zero) |
| Compute (control) | **Azure Kubernetes Service (AKS)** |
| Compute (serverless/bursty) | **Azure Functions** + Durable Tasks |
| Async/eventing | Azure Service Bus, Azure Event Grid |
| IaC | **Bicep** and/or **Terraform** |
| CI/CD | **GitHub Actions** or **Azure DevOps Pipelines** |
| Gateway | Azure API Management + Front Door / WAF |
| Secrets in pipeline | Key Vault + OIDC federated credentials |

---

# Appendix B — Deployment Target Decision Matrix

| Criterion | Azure Container Apps | AKS | Azure Functions |
|-----------|----------------------|-----|-----------------|
| Best for | Most agent APIs, event-driven, microservices | Large multi-team platforms, fine control, service mesh | Bursty/short tasks, glue, schedulers |
| Scaling | KEDA, scale-to-zero (built-in) | HPA/KEDA (you manage) | Per-execution, scale-to-zero |
| Ops burden | Low (managed) | High (you own the cluster) | Lowest |
| Long-running agents | Yes (+ Durable Tasks) | Yes | Use Durable Functions |
| When to choose | **Default for this course's agents** | Need k8s ecosystem/control | Lightweight tools/triggers |

> **Architect's default:** start on **Container Apps**; graduate to **AKS** only when you need cluster-level control, custom networking/service mesh, or multi-team platform governance.

---

# Appendix C — Suggested CI/CD Flow

```
GitHub push ──▶ GitHub Actions
                 ├─ Lint + unit tests (pytest)
                 ├─ Agent eval gate (Foundry Evaluations on golden set)
                 ├─ Build & scan Docker image ──▶ push to ACR
                 ├─ Deploy infra (Bicep/Terraform)
                 └─ Deploy to Container Apps (blue/green) ──▶ smoke test ──▶ promote
```

---

*Designed so students leave able to design, secure, deploy, observe, and operate production multi-agent systems on Azure — the exact competencies an Azure AI Architect is accountable for.*
