"""
    Schema for the result of information extraction
"""

from pydantic import BaseModel


class ExtractionResult(BaseModel):

    intent: str

    state_patch: dict

    missing_fields: list[str]

    confidence: float

    """
    from message + current_state

    return 
    
        intent
        state_patch
        missing_fields

    """