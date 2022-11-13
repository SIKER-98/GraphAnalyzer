from typing import Optional, List

from pydantic import BaseModel


class RelationModel(BaseModel):
    id: Optional[int]
    name: str
    start_node: Optional[int]
    end_node: Optional[int]
    attributes: List[dict] = []
    tags: List[str] = []
