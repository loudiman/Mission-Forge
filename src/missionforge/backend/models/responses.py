from typing import Any

from pydantic import BaseModel, Field


class MissionSummary(BaseModel):
    id: str = Field(..., description="Mission identifier")
    status: str = Field(..., description="Overall mission status")
    goal: str | None = Field(None, description="Mission goal")

class SubMissionSummary(BaseModel):
    id: str = Field(..., description="Sub-mission identifier")
    title: str = Field(..., description="Sub-mission title")
    status: str = Field(..., description="Sub-mission status")

class MissionDetail(BaseModel):
    id: str = Field(..., description="Mission identifier")
    goal: str | None = Field(None, description="Mission goal")
    test_command: str | None = Field(None, description="Test command")
    sub_missions: list[SubMissionSummary] = Field(default_factory=list, description="List of sub-missions")
    aggregate_metrics: dict[str, Any] = Field(default_factory=dict, description="Aggregate metrics")

class SubMissionDetail(BaseModel):
    id: str = Field(..., description="Sub-mission identifier")
    parent: str = Field(..., description="Parent mission identifier")
    title: str = Field(..., description="Sub-mission title")
    goal: str | None = Field(None, description="Sub-mission goal")
    status: str = Field(..., description="Current status")
    depends_on: list[str] = Field(default_factory=list, description="Dependencies")
    tasks: list[str] = Field(default_factory=list, description="Tasks")

class ReportResponse(BaseModel):
    content: str = Field(..., description="Markdown content of the report")
