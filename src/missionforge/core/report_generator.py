"""Mission report generation with Markdown templates."""

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jinja2 import Environment, PackageLoader, select_autoescape

from ..git.operations import get_changed_files_detailed, get_commit_hash, get_diff_stats
from ..models.schemas import ParentMission
from ..schemas.validators import SchemaValidator
from .exceptions import MissionForgeError


class ReportGenerator:
    """Generates PR-ready Markdown evidence reports for missions."""

    def __init__(self) -> None:
        """Initialize report generator with Jinja2 environment."""
        self.env = Environment(
            loader=PackageLoader("missionforge", "templates"),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def generate_report(
        self, mission_path: Path, output_path: Path | None = None
    ) -> tuple[str, Path]:
        """Generate complete mission report.

        Args:
            mission_path: Path to mission directory.
            output_path: Optional custom output path. Defaults to mission_path/report.md.

        Returns:
            Tuple of (report_content, output_file_path).

        Raises:
            MissionForgeError: If report generation fails.
        """
        # Collect all report data
        data = self._collect_report_data(mission_path)

        # Render template
        template = self.env.get_template("mission_report.md.j2")
        report_content = template.render(**data)

        # Determine output path
        if output_path is None:
            output_path = mission_path / "report.md"

        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write report
        try:
            output_path.write_text(report_content, encoding="utf-8")
        except (OSError, PermissionError) as e:
            raise MissionForgeError(
                f"Failed to write report to {output_path}: {e}",
                "Check file permissions and disk space",
            ) from e

        return report_content, output_path

    def _collect_report_data(self, mission_path: Path) -> dict[str, Any]:
        """Collect all data needed for report generation.

        Args:
            mission_path: Path to mission directory.

        Returns:
            Dictionary with all report data.

        Raises:
            MissionForgeError: If data collection fails.
        """
        # Load parent mission
        mission_file = mission_path / "mission.yaml"
        if not mission_file.exists():
            raise MissionForgeError(
                f"Mission file not found: {mission_file}",
                "Ensure mission.yaml exists in the mission directory",
            )

        parent_mission = SchemaValidator.validate_parent_mission_file(mission_file)

        # Load sub-missions
        sub_missions = self._load_sub_missions(mission_path, parent_mission.id)

        # Load validation results
        validation_results = self._load_validation_results(mission_path, sub_missions)

        # Load execution plan if available
        plan = self._load_execution_plan(mission_path)

        # Get git information
        git_info = self._collect_git_info(mission_path)

        # Calculate aggregate status
        overall_status = self._calculate_overall_status(validation_results)

        # Generate dependency diagram
        dependency_diagram = self._generate_dependency_diagram(sub_missions, plan)

        # Collect metrics comparison
        metrics_comparison = self._collect_metrics_comparison(parent_mission, validation_results)

        # Get files changed summary
        files_changed = self._get_files_changed_summary(git_info)

        # Check for forbidden path violations
        forbidden_violations = self._check_forbidden_violations(parent_mission, validation_results)

        # Get next suggested mission if available
        next_mission = self._get_next_mission(mission_path)

        return {
            "mission": parent_mission,
            "sub_missions": sub_missions,
            "validation_results": validation_results,
            "overall_status": overall_status,
            "dependency_diagram": dependency_diagram,
            "metrics_comparison": metrics_comparison,
            "files_changed": files_changed,
            "forbidden_violations": forbidden_violations,
            "next_mission": next_mission,
            "git_info": git_info,
            "generation_timestamp": datetime.now(UTC).isoformat(),
            "cli_version": "0.1.0",
        }

    def _load_sub_missions(self, mission_path: Path, parent_id: str) -> list[dict[str, Any]]:
        """Load all sub-missions for the parent mission.

        Args:
            mission_path: Path to mission directory.
            parent_id: Parent mission ID.

        Returns:
            List of sub-mission data dictionaries.
        """
        sub_missions = []
        sub_missions_dir = mission_path / "sub-missions"

        if not sub_missions_dir.exists():
            return sub_missions

        for sub_file in sorted(sub_missions_dir.glob("*.yaml")):
            try:
                sub_mission = SchemaValidator.validate_sub_mission_file(sub_file)
                if sub_mission.parent == parent_id:
                    sub_missions.append(
                        {
                            "id": sub_mission.id,
                            "title": sub_mission.title,
                            "goal": sub_mission.goal,
                            "depends_on": sub_mission.depends_on,
                            "metrics": sub_mission.metrics,
                            "test_command": sub_mission.test_command,
                        }
                    )
            except Exception:
                # Skip invalid sub-missions
                continue

        return sub_missions

    def _load_validation_results(
        self, mission_path: Path, sub_missions: list[dict[str, Any]]
    ) -> dict[str, dict[str, Any]]:
        """Load validation results for parent and all sub-missions.

        Args:
            mission_path: Path to mission directory.
            sub_missions: List of sub-mission data.

        Returns:
            Dictionary mapping mission IDs to validation results.
        """
        results: dict[str, dict[str, Any]] = {}

        # Load parent validation
        parent_validation_file = mission_path / "validation.json"
        if parent_validation_file.exists():
            try:
                validation = SchemaValidator.validate_validation_file(parent_validation_file)
                results[validation.mission_id] = {
                    "passed": validation.passed,
                    "metrics": validation.metrics.model_dump(),
                    "errors": validation.errors,
                    "timestamp": validation.timestamp,
                }
            except Exception:
                pass

        # Load sub-mission validations
        for sub_mission in sub_missions:
            sub_id = sub_mission["id"]
            sub_validation_file = mission_path / "sub-missions" / f"{sub_id}.validation.json"
            if sub_validation_file.exists():
                try:
                    validation = SchemaValidator.validate_validation_file(sub_validation_file)
                    results[sub_id] = {
                        "passed": validation.passed,
                        "metrics": validation.metrics.model_dump(),
                        "errors": validation.errors,
                        "timestamp": validation.timestamp,
                    }
                except Exception:
                    pass

        return results

    def _load_execution_plan(self, mission_path: Path) -> dict[str, Any] | None:
        """Load execution plan if available.

        Args:
            mission_path: Path to mission directory.

        Returns:
            Execution plan data or None if not available.
        """
        plan_file = mission_path / "plan.yaml"
        if not plan_file.exists():
            return None

        try:
            plan = SchemaValidator.validate_plan_file(plan_file)
            return {
                "execution_order": plan.execution_order,
                "dependency_graph": plan.dependency_graph,
            }
        except Exception:
            return None

    def _collect_git_info(self, mission_path: Path) -> dict[str, Any]:
        """Collect git information for the mission.

        Args:
            mission_path: Path to mission directory.

        Returns:
            Dictionary with git information.
        """
        try:
            commit_hash = get_commit_hash(cwd=mission_path)
            diff_stats = get_diff_stats(cwd=mission_path)
            changed_files = get_changed_files_detailed(cwd=mission_path)

            return {
                "commit_hash": commit_hash[:7],
                "full_commit_hash": commit_hash,
                "files_changed": diff_stats["files_changed"],
                "insertions": diff_stats["insertions"],
                "deletions": diff_stats["deletions"],
                "added_files": [str(f) for f in changed_files["added"]],
                "modified_files": [str(f) for f in changed_files["modified"]],
                "deleted_files": [str(f) for f in changed_files["deleted"]],
                "renamed_files": [str(f) for f in changed_files["renamed"]],
            }
        except Exception:
            return {
                "commit_hash": "unknown",
                "full_commit_hash": "unknown",
                "files_changed": 0,
                "insertions": 0,
                "deletions": 0,
                "added_files": [],
                "modified_files": [],
                "deleted_files": [],
                "renamed_files": [],
            }

    def _calculate_overall_status(self, validation_results: dict[str, dict[str, Any]]) -> str:
        """Calculate overall mission status from validation results.

        Args:
            validation_results: Validation results for all missions.

        Returns:
            Overall status: "PASSED", "FAILED", or "INCOMPLETE".
        """
        if not validation_results:
            return "INCOMPLETE"

        all_passed = all(result["passed"] for result in validation_results.values())
        return "PASSED" if all_passed else "FAILED"

    def _generate_dependency_diagram(
        self, sub_missions: list[dict[str, Any]], plan: dict[str, Any] | None
    ) -> str:
        """Generate ASCII dependency diagram.

        Args:
            sub_missions: List of sub-mission data.
            plan: Execution plan data.

        Returns:
            ASCII diagram as string.
        """
        if not sub_missions:
            return "No sub-missions"

        # Simple ASCII diagram showing dependencies
        lines = []
        for sub_mission in sub_missions:
            sub_id = sub_mission["id"]
            deps = sub_mission.get("depends_on", [])
            if deps:
                dep_str = ", ".join(deps)
                lines.append(f"{sub_id} (depends on: {dep_str})")
            else:
                lines.append(f"{sub_id} (no dependencies)")

        return "\n".join(lines)

    def _collect_metrics_comparison(
        self, parent_mission: ParentMission, validation_results: dict[str, dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Collect metrics comparison data.

        Args:
            parent_mission: Parent mission with aggregate metrics.
            validation_results: Validation results.

        Returns:
            List of metric comparison dictionaries.
        """
        comparisons = []

        for metric_name, metric_def in parent_mission.aggregate_metrics.items():
            # Get final value from validation results
            final_value = None
            for result in validation_results.values():
                custom_metrics = result.get("metrics", {}).get("custom_metrics", {})
                if metric_name in custom_metrics:
                    final_value = custom_metrics[metric_name]
                    break

            # Determine status
            status = "UNKNOWN"
            if final_value is not None:
                if metric_def.target is not None:
                    status = "PASSED" if final_value == metric_def.target else "FAILED"
                elif metric_def.min is not None and metric_def.max is not None:
                    status = (
                        "PASSED" if metric_def.min <= final_value <= metric_def.max else "FAILED"
                    )
                elif metric_def.min is not None:
                    status = "PASSED" if final_value >= metric_def.min else "FAILED"
                elif metric_def.max is not None:
                    status = "PASSED" if final_value <= metric_def.max else "FAILED"

            comparisons.append(
                {
                    "name": metric_name,
                    "target": metric_def.target,
                    "min": metric_def.min,
                    "max": metric_def.max,
                    "final": final_value,
                    "status": status,
                }
            )

        return comparisons

    def _get_files_changed_summary(self, git_info: dict[str, Any]) -> dict[str, Any]:
        """Get summary of files changed.

        Args:
            git_info: Git information dictionary.

        Returns:
            Files changed summary.
        """
        all_files = (
            git_info.get("added_files", [])
            + git_info.get("modified_files", [])
            + git_info.get("deleted_files", [])
            + git_info.get("renamed_files", [])
        )

        return {
            "total": len(all_files),
            "added": len(git_info.get("added_files", [])),
            "modified": len(git_info.get("modified_files", [])),
            "deleted": len(git_info.get("deleted_files", [])),
            "renamed": len(git_info.get("renamed_files", [])),
            "files": all_files,
        }

    def _check_forbidden_violations(
        self, parent_mission: ParentMission, validation_results: dict[str, dict[str, Any]]
    ) -> list[str]:
        """Check for forbidden path violations.

        Args:
            parent_mission: Parent mission with forbidden paths.
            validation_results: Validation results.

        Returns:
            List of violation messages.
        """
        violations = []

        for mission_id, result in validation_results.items():
            errors = result.get("errors", [])
            for error in errors:
                if "forbidden" in error.lower() or "path" in error.lower():
                    violations.append(f"{mission_id}: {error}")

        return violations

    def _get_next_mission(self, mission_path: Path) -> str | None:
        """Get next suggested mission if available.

        Args:
            mission_path: Path to mission directory.

        Returns:
            Next mission ID or None.
        """
        next_mission_file = mission_path / "next_mission.txt"
        if next_mission_file.exists():
            return next_mission_file.read_text(encoding="utf-8").strip()
        return None


# Made with Bob
