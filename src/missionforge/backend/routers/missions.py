from fastapi import APIRouter, HTTPException, Depends, Path
from typing import List

from ..repository import MissionRepository
from ..models.responses import MissionSummary, MissionDetail, SubMissionSummary, SubMissionDetail, ReportResponse

router = APIRouter(prefix="/api/missions", tags=["missions"])

def get_repository() -> MissionRepository:
    repo = MissionRepository()
    if not repo.missionforge_dir.exists():
        raise HTTPException(status_code=500, detail="MissionForge repository not found")
    return repo

@router.get("", response_model=List[MissionSummary])
def list_missions(repo: MissionRepository = Depends(get_repository)):
    """List all parent missions."""
    try:
        missions = repo.list_missions()
        result = []
        for m_id in missions:
            # We would read validation.json for status, but simplify for now
            result.append(MissionSummary(id=m_id, status="UNKNOWN"))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{mission_id}", response_model=MissionDetail)
def get_mission(
    mission_id: str = Path(..., description="The ID of the parent mission"),
    repo: MissionRepository = Depends(get_repository)
):
    """Get details of a specific parent mission."""
    mission_yaml = repo.read_mission_yaml(mission_id)
    if not mission_yaml:
        raise HTTPException(status_code=404, detail=f"Mission {mission_id} not found")
    
    return MissionDetail(
        id=mission_yaml.get("id", mission_id),
        goal=mission_yaml.get("goal"),
        test_command=mission_yaml.get("test_command"),
        sub_missions=[
            SubMissionSummary(id=sub_id, title=sub_id, status="UNKNOWN")
            for sub_id in mission_yaml.get("sub_missions", [])
        ],
        aggregate_metrics=mission_yaml.get("aggregate_metrics", {})
    )

@router.get("/{mission_id}/sub-missions", response_model=List[SubMissionSummary])
def list_sub_missions(
    mission_id: str = Path(..., description="The ID of the parent mission"),
    repo: MissionRepository = Depends(get_repository)
):
    """List all sub-missions for a specific parent mission."""
    mission_yaml = repo.read_mission_yaml(mission_id)
    if not mission_yaml:
        raise HTTPException(status_code=404, detail=f"Mission {mission_id} not found")
    
    sub_missions = mission_yaml.get("sub_missions", [])
    result = []
    for sub_id in sub_missions:
        sub_yaml = repo.read_sub_mission_yaml(mission_id, sub_id)
        if sub_yaml:
            result.append(SubMissionSummary(
                id=sub_id,
                title=sub_yaml.get("title", ""),
                status="UNKNOWN"
            ))
        else:
            result.append(SubMissionSummary(id=sub_id, title="", status="UNKNOWN"))
    return result

@router.get("/{mission_id}/sub-missions/{sub_id}", response_model=SubMissionDetail)
def get_sub_mission(
    mission_id: str = Path(..., description="The ID of the parent mission"),
    sub_id: str = Path(..., description="The ID of the sub-mission"),
    repo: MissionRepository = Depends(get_repository)
):
    """Get details of a specific sub-mission."""
    sub_yaml = repo.read_sub_mission_yaml(mission_id, sub_id)
    if not sub_yaml:
        raise HTTPException(status_code=404, detail=f"Sub-mission {sub_id} not found for mission {mission_id}")
    
    return SubMissionDetail(
        id=sub_yaml.get("id", sub_id),
        parent=sub_yaml.get("parent", mission_id),
        title=sub_yaml.get("title", ""),
        goal=sub_yaml.get("goal"),
        status="UNKNOWN",
        depends_on=sub_yaml.get("depends_on", []),
        tasks=sub_yaml.get("tasks", [])
    )

@router.get("/{mission_id}/report", response_model=ReportResponse)
def get_report(
    mission_id: str = Path(..., description="The ID of the parent mission"),
    repo: MissionRepository = Depends(get_repository)
):
    """Get the markdown report for a mission."""
    report_content = repo.read_report(mission_id)
    if report_content is None:
        raise HTTPException(status_code=404, detail=f"Report not found for mission {mission_id}")
    
    return ReportResponse(content=report_content)
