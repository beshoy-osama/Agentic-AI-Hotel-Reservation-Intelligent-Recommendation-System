from enum import Enum


class AgentAction(str, Enum):
    """Actions the agent can select at each turn."""

    ASK_MISSING_INFORMATION = "ASK_MISSING_INFORMATION"
    SEARCH_ROOMS = "SEARCH_ROOMS"
