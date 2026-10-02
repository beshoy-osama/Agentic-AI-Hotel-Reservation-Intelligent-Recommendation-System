"""
Unit tests for ActionSelector.
"""

import pytest

from Orchestrator.ActionSelector import ActionSelector
from enums.AgentAction import AgentAction


@pytest.fixture
def selector() -> ActionSelector:
    return ActionSelector()


def test_missing_fields_returns_ask_missing(selector: ActionSelector):
    result = selector.select(missing_fields=["check_in", "adults"])
    assert result == AgentAction.ASK_MISSING_INFORMATION


def test_single_missing_field_returns_ask_missing(selector: ActionSelector):
    result = selector.select(missing_fields=["children"])
    assert result == AgentAction.ASK_MISSING_INFORMATION


def test_no_missing_fields_returns_search_rooms(selector: ActionSelector):
    result = selector.select(missing_fields=[])
    assert result == AgentAction.SEARCH_ROOMS


def test_return_type_is_agent_action(selector: ActionSelector):
    result = selector.select(missing_fields=[])
    assert isinstance(result, AgentAction)
