from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class MissionSummary(BaseModel):
    id: str = Field(..., description="Mission identifier")
    status: str = Field(..., description="Overall mission status")
    goal: Optional[str] = Field(None, description="Mission goal")

class SubMissionSummary(BaseModel):
    id: str = Field(..., description="Sub-mission identifier")
    title: str = Field(..., description="Sub-mission title")
    status: str = Field(..., description="Sub-mission status")

class MissionDetail(BaseModel):
    id: str = Field(..., description="Mission identifier")
    goal: Optional[str] = Field(None, description="Mission goal")
    test_command: Optional[str] = Field(None, description="Test command")
    sub_missions: List[SubMissionSummary] = Field(default_factory=list, description="List of sub-missions")
    aggregate_metrics: Dict[str, Any] = Field(default_factory=dict, description="Aggregate metrics")

class SubMissionDetail(BaseModel):
    id: str = Field(..., description="Sub-mission identifier")
    parent: str = Field(..., description="Parent mission identifier")
    title: str = Field(..., description="Sub-mission title")
    goal: Optional[str] = Field(None, description="Sub-mission goal")
    status: str = Field(..., description="Current status")
    depends_on: List[str] = Field(default_factory=list, description="Dependencies")
    tasks: List[str] = Field(default_factory=list, description="Tasks")

class ReportResponse(BaseModel):
    content: str = Field(..., description="Markdown content of the report")
