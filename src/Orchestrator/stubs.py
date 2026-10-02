"""
Temporary stub services for development.

These satisfy the AI3 ports with no-op implementations
so the endpoint can start and be tested while AI3 is not yet built.

Replace with real AI3 services when available.
"""

from schemas.state import ConversationState
from schemas.extraction import ExtractionResult


class StubExtractionService:
    """No-op extraction — returns unknown intent with no patches."""

    async def extract(
        self,
        message: str,
        current_state: ConversationState,
    ) -> ExtractionResult:
        return ExtractionResult(
            intent="unknown",
            state_patch={},
            missing_fields=[],
            confidence=0.0,
        )


class StubStateService:
    """No-op state service — returns the state unchanged."""

    def apply_patch(
        self,
        current_state: ConversationState,
        state_patch: dict,
        intent: str | None = None,
    ) -> ConversationState:
        return current_state
