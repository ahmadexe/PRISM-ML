from pydantic import BaseModel

class Image(BaseModel):
    url: str
    post_id: int = None