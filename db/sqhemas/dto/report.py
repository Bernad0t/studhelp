from datetime import datetime

from pydantic import BaseModel

from db.sqhemas.enums.workload import Workload


class ReportsDTO(BaseModel):
    id: int
    date_created: datetime
    time_reaction: str
    workload: Workload