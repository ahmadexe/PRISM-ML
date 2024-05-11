from pydantic import BaseModel

class Text(BaseModel):
    text: str
    post_id: int = None