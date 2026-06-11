"""Week 1 — IT Helpdesk Triage Agent endpoint.

Exposes the core agent loop as a REST API, demonstrating the agent contract:
inputs (a message), a tool (KB lookup), guardrails (escalation), and a typed
success criterion (the structured response).
"""

from fastapi import APIRouter

from app.config import get_settings
from app.core.agent_loop import run_helpdesk_agent
from app.schemas.agent import AgentStepOut, HelloRequest, HelloResponse

router = APIRouter(prefix="/api/v1", tags=["week01-foundations"])


@router.post("/hello", response_model=HelloResponse)
def hello_agent(payload: HelloRequest) -> HelloResponse:
    """Triage an incoming support message and either answer or escalate."""
    result = run_helpdesk_agent(payload.message)
    settings = get_settings()
    return HelloResponse(
        answer=result.answer,
        category=result.category,
        escalated=result.escalated,
        steps=[AgentStepOut(phase=s.phase, detail=s.detail) for s in result.steps],
        mode="azure-openai" if settings.use_azure_openai else "mock",
    )
