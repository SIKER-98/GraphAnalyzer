from typing import Optional

from pydantic import BaseModel


class GraphModel(BaseModel):
    id: Optional[int]
    name: str
    description: str
