"""
Agent response schema returned by the orchestrator.
"""

from pydantic import BaseModel

from enums.AgentAction import AgentAction


class AgentResponse(BaseModel):
    """Response returned by AgentOrchestrator.process()."""

    assistant_message: str
    next_action: AgentAction
    state_patch: dict
    missing_fields: list[str]
