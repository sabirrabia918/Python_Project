from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Launch(BaseModel):
    id: str
    name: str
    status: str
    agency: str
    agency_type: Optional[str] = None
    net: datetime
    fail_reason: Optional[str] = None
    mission_type: Optional[str] = None