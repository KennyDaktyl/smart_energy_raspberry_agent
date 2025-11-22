from pydantic import BaseModel
from typing import List, Dict, Any


class HeartbeatPayload(BaseModel):
    uuid: str
    devices: List[Dict[str, Any]]
