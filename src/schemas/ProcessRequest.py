from pydantic import BaseModel


class ProcessRequest(BaseModel):
    message: str
    current_state: dict 