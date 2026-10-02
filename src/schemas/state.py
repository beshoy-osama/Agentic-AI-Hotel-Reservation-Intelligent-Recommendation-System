"""
    Conversation state schema
"""

from pydantic import BaseModel
from typing import Optional

class Preferences(BaseModel):
    room_type: Optional[str] = None
    view: Optional[str] = None
    breakfast: Optional[bool] = None
    balcony: Optional[bool] = None
    bed_type: Optional[str] = None
    accessible: Optional[bool] = None

class ConversationState(BaseModel):
    intent: Optional[str] = None

    check_in: Optional[str] = None
    check_out: Optional[str] = None

    adults: Optional[int] = None
    children: Optional[int] = None

    budget: Optional[float] = None

    preferences: Preferences = Preferences()

    rooms_presented: list[str] = []
    selected_room_id: Optional[str] = None

    current_objection: Optional[str] = None
    booking_stage: str = "COLLECTING_REQUIREMENTS"

