"""
Unit tests for AgentOrchestrator (AI1).

All tests use FakeExtractionService and FakeStateService.
No real AI3 implementation is imported.
"""

import pytest
from pydantic import ValidationError

from Orchestrator.AgentOrchestratorController import AgentOrchestratorController
from enums.AgentAction import AgentAction
from schemas.extraction import ExtractionResult
from schemas.agent_response import AgentResponse
from schemas.state import ConversationState

from tests.fakes.fake_extraction_service import FakeExtractionService
from tests.fakes.fake_state_service import FakeStateService


def _make_orchestrator(
    extraction_result: ExtractionResult,
    patched_state: ConversationState | None = None,
) -> tuple[AgentOrchestratorController, FakeExtractionService, FakeStateService]:
    """Helper: build an orchestrator wired to configurable fakes."""
    fake_extraction = FakeExtractionService(result=extraction_result)
    fake_state = FakeStateService(patched_state=patched_state)
    orch = AgentOrchestratorController(
        extraction_service=fake_extraction,
        state_service=fake_state,
    )
    return orch, fake_extraction, fake_state


# ══════════════════════════════════════════════════════════════════════
#  TEST 1 — All booking fields missing
# ══════════════════════════════════════════════════════════════════════

async def test_all_fields_missing_returns_ask_missing():
    """When all core fields are missing, action is ASK_MISSING_INFORMATION
    and the question mentions all fields in ONE turn."""

    orch, _, _ = _make_orchestrator(
        ExtractionResult(
            intent="SEARCH_ROOM",
            state_patch={},
            missing_fields=["check_in", "check_out", "adults", "children"],
            confidence=0.9,
        ),
    )

    result = await orch.process(message="I want to book a room", current_state={})

    assert isinstance(result, AgentResponse)
    assert result.next_action == AgentAction.ASK_MISSING_INFORMATION

    msg = result.assistant_message.lower()
    assert "check-in" in msg
    assert "check-out" in msg
    assert "adults" in msg
    assert "children" in msg

    # Must be ONE combined question, not multiple sentences
    assert result.assistant_message.count("?") == 1


# ══════════════════════════════════════════════════════════════════════
#  TEST 2 — State complete → SEARCH_ROOMS
# ══════════════════════════════════════════════════════════════════════

async def test_no_missing_fields_returns_search_rooms():
    """When no fields are missing, action is SEARCH_ROOMS."""

    orch, _, _ = _make_orchestrator(
        ExtractionResult(
            intent="SEARCH_ROOM",
            state_patch={},
            missing_fields=[],
            confidence=0.95,
        ),
    )

    result = await orch.process(message="Find me a room", current_state={})

    assert result.next_action == AgentAction.SEARCH_ROOMS
    assert result.assistant_message == ""


# ══════════════════════════════════════════════════════════════════════
#  TEST 3 — Children only missing
# ══════════════════════════════════════════════════════════════════════

async def test_children_only_missing():
    """When only children is missing, question asks about children only."""

    orch, _, _ = _make_orchestrator(
        ExtractionResult(
            intent="SEARCH_ROOM",
            state_patch={},
            missing_fields=["children"],
            confidence=0.9,
        ),
    )

    result = await orch.process(message="Book a room", current_state={})

    assert result.next_action == AgentAction.ASK_MISSING_INFORMATION

    msg = result.assistant_message.lower()
    assert "children" in msg

    # Should NOT mention adults, dates, etc.
    assert "adults" not in msg
    assert "check-in" not in msg
    assert "check-out" not in msg


# ══════════════════════════════════════════════════════════════════════
#  TEST 4 — Multiple partial fields
# ══════════════════════════════════════════════════════════════════════

async def test_partial_missing_fields():
    """When check_out + children are missing, ONE question asks both."""

    orch, _, _ = _make_orchestrator(
        ExtractionResult(
            intent="SEARCH_ROOM",
            state_patch={},
            missing_fields=["check_out", "children"],
            confidence=0.9,
        ),
    )

    result = await orch.process(message="I need a room", current_state={})

    assert result.next_action == AgentAction.ASK_MISSING_INFORMATION

    msg = result.assistant_message.lower()
    assert "check-out" in msg
    assert "children" in msg
    assert result.assistant_message.count("?") == 1


# ══════════════════════════════════════════════════════════════════════
#  TEST 5 — AI3 extraction patch forwarded to StateService
# ══════════════════════════════════════════════════════════════════════

async def test_extraction_patch_passed_to_state_service():
    """AI1 must forward the state_patch and intent to StateService
    without performing the merge itself."""

    orch, _, fake_state = _make_orchestrator(
        ExtractionResult(
            intent="SEARCH_ROOM",
            state_patch={"preferences": {"view": "sea"}},
            missing_fields=[],
            confidence=0.9,
        ),
    )

    await orch.process(
        message="I want a sea view room",
        current_state={},
    )

    assert fake_state.last_call is not None
    assert fake_state.last_call["state_patch"] == {"preferences": {"view": "sea"}}
    assert fake_state.last_call["intent"] == "SEARCH_ROOM"


# ══════════════════════════════════════════════════════════════════════
#  TEST 6 — Invalid incoming state raises ValidationError
# ══════════════════════════════════════════════════════════════════════

async def test_invalid_state_raises_validation_error():
    """Malformed state must cause a ValidationError, NOT be silently
    replaced with default state."""

    orch, _, _ = _make_orchestrator(
        ExtractionResult(
            intent="unknown",
            state_patch={},
            missing_fields=[],
            confidence=0.0,
        ),
    )

    with pytest.raises(ValidationError):
        await orch.process(
            message="hello",
            current_state={"adults": "not_a_number"},
        )


# ══════════════════════════════════════════════════════════════════════
#  TEST 7 — Dependency separation (works with fakes only)
# ══════════════════════════════════════════════════════════════════════

async def test_works_with_fakes_without_real_ai3():
    """AgentOrchestrator must function entirely with
    FakeExtractionService and FakeStateService — no real AI3 code."""

    orch, _, _ = _make_orchestrator(
        ExtractionResult(
            intent="SEARCH_ROOM",
            state_patch={"check_in": "2026-12-01"},
            missing_fields=[],
            confidence=0.85,
        ),
    )

    result = await orch.process(
        message="hello",
        current_state={},
    )

    assert isinstance(result, AgentResponse)
    assert result.next_action == AgentAction.SEARCH_ROOMS
    assert result.state_patch == {"check_in": "2026-12-01"}
    assert result.missing_fields == []
