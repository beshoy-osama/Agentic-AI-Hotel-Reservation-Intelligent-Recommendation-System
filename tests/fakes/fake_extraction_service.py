"""
Configurable fake extraction service for testing AI1.

This is NOT an AI3 implementation.
It returns a predetermined ExtractionResult for deterministic testing.
"""

from schemas.state import ConversationState
from schemas.extraction import ExtractionResult


class FakeExtractionService:

    def __init__(self, result: ExtractionResult):
        self._result = result
        self.last_call: dict | None = None

    async def extract(
        self,
        message: str,
        current_state: ConversationState,
    ) -> ExtractionResult:
        self.last_call = {
            "message": message,
            "current_state": current_state,
        }
        return self._result
