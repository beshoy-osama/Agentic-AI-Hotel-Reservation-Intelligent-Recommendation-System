"""
Unit tests for MissingFieldsPolicy.
"""

import pytest

from Orchestrator.MissingFieldsPolicy import MissingFieldsPolicy


@pytest.fixture
def policy() -> MissingFieldsPolicy:
    return MissingFieldsPolicy()


# ── Grouping tests ────────────────────────────────────────────────────

def test_dates_grouped(policy: MissingFieldsPolicy):
    """check_in + check_out should be grouped into one phrase."""
    question = policy.build_question(["check_in", "check_out"])

    assert "check-in" in question.lower()
    assert "check-out" in question.lower()
    assert "dates" in question.lower()
    assert question.count("?") == 1


def test_guests_grouped(policy: MissingFieldsPolicy):
    """adults + children should be grouped into one phrase."""
    question = policy.build_question(["adults", "children"])

    assert "adults" in question.lower()
    assert "children" in question.lower()
    assert question.count("?") == 1


def test_all_four_grouped(policy: MissingFieldsPolicy):
    """All core fields should produce two groups in one question."""
    question = policy.build_question(
        ["check_in", "check_out", "adults", "children"],
    )

    assert "check-in" in question.lower()
    assert "check-out" in question.lower()
    assert "adults" in question.lower()
    assert "children" in question.lower()
    assert question.count("?") == 1


# ── Partial / individual tests ────────────────────────────────────────

def test_children_only(policy: MissingFieldsPolicy):
    """Single field produces a standalone question."""
    question = policy.build_question(["children"])

    assert "children" in question.lower()
    assert "adults" not in question.lower()
    assert question.count("?") == 1


def test_check_out_only(policy: MissingFieldsPolicy):
    question = policy.build_question(["check_out"])

    assert "check-out" in question.lower()
    assert "check-in" not in question.lower()


def test_partial_cross_group(policy: MissingFieldsPolicy):
    """check_out + children: no group matches, two individual labels."""
    question = policy.build_question(["check_out", "children"])

    assert "check-out" in question.lower()
    assert "children" in question.lower()
    assert question.count("?") == 1


# ── No internal field names exposed ──────────────────────────────────

def test_no_underscored_field_names(policy: MissingFieldsPolicy):
    """Customer-facing text must NOT contain raw field names."""
    question = policy.build_question(
        ["check_in", "check_out", "adults", "children"],
    )

    assert "check_in" not in question
    assert "check_out" not in question


# ── Empty input ──────────────────────────────────────────────────────

def test_empty_input_returns_empty_string(policy: MissingFieldsPolicy):
    assert policy.build_question([]) == ""


# ── Budget / preferences ─────────────────────────────────────────────

def test_budget_field(policy: MissingFieldsPolicy):
    question = policy.build_question(["budget"])

    assert "budget" in question.lower()
    assert question.count("?") == 1


def test_mixed_group_and_individual(policy: MissingFieldsPolicy):
    """Group (dates) + individual (budget) in one question."""
    question = policy.build_question(["check_in", "check_out", "budget"])

    assert "check-in" in question.lower()
    assert "check-out" in question.lower()
    assert "budget" in question.lower()
    assert question.count("?") == 1
