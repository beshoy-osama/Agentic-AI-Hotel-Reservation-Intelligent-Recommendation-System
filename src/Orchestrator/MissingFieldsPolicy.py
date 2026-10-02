"""
Missing-fields question policy.

AI3 decides WHAT is missing.
AI1 decides HOW to ask for it.

Rules:
- Ask for ALL missing fields in ONE turn.
- Group related fields into natural phrases.
- Never expose internal field names (e.g. check_in) to the customer.
"""


class MissingFieldsPolicy:

    _FIELD_GROUPS: list[dict] = [
        {
            "fields": {"check_in", "check_out"},
            "phrase": "your check-in and check-out dates",
        },
        {
            "fields": {"adults", "children"},
            "phrase": "the number of adults and children",
        },
    ]

    _FIELD_LABELS: dict[str, str] = {
        "check_in": "your check-in date",
        "check_out": "your check-out date",
        "adults": "the number of adults",
        "children": "the number of children",
        "budget": "your budget",
        "room_type": "your preferred room type",
        "view": "your view preference",
        "breakfast": "your breakfast preference",
        "balcony": "your balcony preference",
        "bed_type": "your preferred bed type",
        "accessible": "your accessibility needs",
    }

    def build_question(self, missing_fields: list[str]) -> str:
        """
        Build a single customer-facing question asking for all missing fields.

        Groups related fields (e.g. check_in + check_out → dates) and
        falls back to individual labels for ungrouped fields.
        """
        if not missing_fields:
            return ""

        parts: list[str] = []
        used: set[str] = set()
        missing_set = set(missing_fields)

        # ── Match groups first ────────────────────────────────────────
        for group in self._FIELD_GROUPS:
            if group["fields"].issubset(missing_set):
                parts.append(group["phrase"])
                used.update(group["fields"])

        # ── Individual fields ─────────────────────────────────────────
        for field in missing_fields:
            if field not in used:
                label = self._FIELD_LABELS.get(
                    field, field.replace("_", " "),
                )
                parts.append(label)

        combined = self._join(parts)
        return f"Could you please provide {combined}?"

    @staticmethod
    def _join(parts: list[str]) -> str:
        if len(parts) == 1:
            return parts[0]
        if len(parts) == 2:
            return f"{parts[0]} and {parts[1]}"
        return ", ".join(parts[:-1]) + f", and {parts[-1]}"
