"""Pydantic request/response contracts — the agent's typed API surface."""

from pydantic import BaseModel, Field


class HelloRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Incoming support ticket / user message.")


class AgentStepOut(BaseModel):
    phase: str
    detail: str


class HelloResponse(BaseModel):
    answer: str
    category: str
    escalated: bool
    steps: list[AgentStepOut]
    mode: str = Field(..., description="'azure-openai' or 'mock' depending on configuration.")
