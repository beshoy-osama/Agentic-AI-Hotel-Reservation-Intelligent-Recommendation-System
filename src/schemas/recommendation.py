from pydantic import BaseModel


class RoomCandidate(BaseModel):
    room_id: str
    room_type: str
    total_price: float

    max_adults: int
    max_children: int

    view: str | None = None
    breakfast_included: bool = False
    balcony: bool = False


class RankedRoom(BaseModel):
    room_id: str
    rank: int
    score: float
    reason_codes: list[str]


class RecommendationResult(BaseModel):
    ranked_rooms: list[RankedRoom]
    recommended_action: str