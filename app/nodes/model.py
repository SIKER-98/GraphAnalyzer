from typing import Optional, List

from pydantic import BaseModel


class NodeModel(BaseModel):
    id: Optional[int]
    name: str
    text_attributes: List[dict] = []
    number_attributes: List[dict] = []
    tags: List[str] = []



