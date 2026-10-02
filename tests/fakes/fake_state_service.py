"""
Configurable fake state service for testing AI1.

This is NOT an AI3 implementation.
It returns a predetermined ConversationState
and records the arguments for test assertions.
"""

from schemas.state import ConversationState


class FakeStateService:

    def __init__(self, patched_state: ConversationState | None = None):
        self._patched_state = patched_state or ConversationState()
        self.last_call: dict | None = None

    def apply_patch(
        self,
        current_state: ConversationState,
        state_patch: dict,
        intent: str | None = None,
    ) -> ConversationState:
        self.last_call = {
            "current_state": current_state,
            "state_patch": state_patch,
            "intent": intent,
        }
        return self._patched_state
