from pydantic import BaseModel
from typing import Optional


class SolverResult(BaseModel):
    status: Optional[str]
    objective_value: Optional[float]
    runtime: Optional[float]  # in seconds
    memory_used_MB: Optional[float]
    error: Optional[str] = None

    solver: Optional[str] = None
    additional_info: Optional[dict] = None
