from pydantic import BaseModel
from typing import Optional

class WatchedFolder(BaseModel):
    path: str
    name: str
    description: Optional[str] = None