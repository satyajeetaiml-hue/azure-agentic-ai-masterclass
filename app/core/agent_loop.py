"""The core agent loop: reason → plan → act → observe.

This is the conceptual heart of Week 1. It demonstrates the agent pattern with
a single tool (a mock knowledge-base lookup) and a reasoning step that decides
whether to *answer* from the KB or *escalate* to a human.

When Azure OpenAI is configured (see ``Settings.use_azure_openai``) the reasoning
step calls the model; otherwise it uses a deterministic heuristic so the project
runs with zero cloud dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# A tiny mock "knowledge base" standing in for Azure AI Search (added in Week 8).
_MOCK_KB: dict[str, str] = {
    "vpn": "Reset your VPN client, then reconnect using your corporate credentials. "
    "If it still fails, clear the cached profile under Settings → Network.",
    "password": "Use the self-service portal at /reset to change your password. "
    "Locked accounts auto-unlock after 30 minutes.",
    "email": "Outlook issues are usually fixed by restarting the app and re-adding "
    "the account. Check service health if multiple users are affected.",
}

# Keywords that imply urgency / risk → escalate rather than auto-answer.
_ESCALATION_SIGNALS = ("urgent", "down", "outage", "breach", "production", "asap")


@dataclass
class AgentStep:
    """A single observable step in the agent loop (useful for tracing later)."""

    phase: str  # reason | plan | act | observe
    detail: str


@dataclass
class AgentResult:
    answer: str
    category: str
    escalated: bool
    steps: list[AgentStep] = field(default_factory=list)


def _kb_lookup(query: str) -> tuple[str, str | None]:
    """The agent's single tool. Returns (matched_category, answer | None)."""
    lowered = query.lower()
    for key, value in _MOCK_KB.items():
        if key in lowered:
            return key, value
    return "general", None


def _classify(query: str) -> str:
    lowered = query.lower()
    if any(sig in lowered for sig in _ESCALATION_SIGNALS):
        return "high"
    return "normal"


def run_helpdesk_agent(message: str) -> AgentResult:
    """Run the Week 1 IT-helpdesk triage agent loop over an incoming message."""
    steps: list[AgentStep] = []
    settings = get_settings()

    # 1) REASON — assess severity.
    severity = _classify(message)
    steps.append(AgentStep("reason", f"Assessed severity as '{severity}'."))

    # 2) PLAN — decide whether to use the KB tool or escalate.
    plan = "escalate" if severity == "high" else "answer_from_kb"
    steps.append(AgentStep("plan", f"Chosen strategy: {plan}."))

    # 3) ACT — call the tool.
    category, kb_answer = _kb_lookup(message)
    steps.append(
        AgentStep("act", f"KB lookup → category='{category}', hit={kb_answer is not None}.")
    )

    # 4) OBSERVE — form the final response.
    if plan == "escalate":
        answer = (
            "This looks time-sensitive, so I'm escalating it to a human engineer "
            f"and have logged it under category '{category}'."
        )
        result = AgentResult(answer=answer, category=category, escalated=True, steps=steps)
    elif kb_answer:
        answer = kb_answer
        result = AgentResult(answer=answer, category=category, escalated=False, steps=steps)
    else:
        answer = (
            "I couldn't find a matching knowledge-base article, so I'm routing this "
            "to the helpdesk queue for a human to review."
        )
        result = AgentResult(answer=answer, category=category, escalated=True, steps=steps)

    steps.append(AgentStep("observe", f"Final decision: escalated={result.escalated}."))

    mode = "azure-openai" if settings.use_azure_openai else "mock"
    logger.info("helpdesk agent ran in %s mode (category=%s)", mode, result.category)
    return result
