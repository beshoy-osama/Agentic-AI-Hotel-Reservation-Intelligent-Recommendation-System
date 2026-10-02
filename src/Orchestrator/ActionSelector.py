"""
Action selector for the agent orchestrator.

MVP actions: ASK_MISSING_INFORMATION, SEARCH_ROOMS.
"""

from enums.AgentAction import AgentAction


class ActionSelector:
    """
    Selects the next action based on the current extraction result.

    Rule (MVP):
        missing_fields → ASK_MISSING_INFORMATION
        no missing      → SEARCH_ROOMS
    """

    def select(self, missing_fields: list[str]) -> AgentAction:
        if missing_fields:
            return AgentAction.ASK_MISSING_INFORMATION
        return AgentAction.SEARCH_ROOMS
