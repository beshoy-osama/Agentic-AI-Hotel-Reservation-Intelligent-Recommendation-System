"""
Ports (interfaces) that AI1 uses to communicate with AI3.

AI1 OWNS these interfaces.
AI3 IMPLEMENTS them later.

AI1 must never contain extraction or state-merge logic.
"""

from typing import Protocol

from schemas.state import ConversationState
from schemas.extraction import ExtractionResult


class ExtractionServicePort(Protocol):
    """
    Contract for the extraction service (AI3).

    Responsible for:
    - Intent detection
    - Requirement extraction
    - Missing-fields detection
    """

    async def extract(
        self,
        message: str,
        current_state: ConversationState,
    ) -> ExtractionResult: ...


class StateServicePort(Protocol):
    """
    Contract for the state service (AI3).

    Responsible for:
    - Applying a state patch to a ConversationState
    - Merging nested fields (e.g. preferences)
    - Setting the intent
    """

    def apply_patch(
        self,
        current_state: ConversationState,
        state_patch: dict,
        intent: str | None = None,
    ) -> ConversationState: ...
