"""Unit tests for ValidationService metric logic."""

from unittest.mock import MagicMock

from missionforge.core.validation_service import ValidationService
from missionforge.core.workspace import Workspace
from missionforge.models.schemas import (
    DeterministicEvidence,
    ScopeCheckResult,
    SubMissionValidation,
    TestResults,
    ValidationMetric,
)


def _make_service() -> ValidationService:
    """Create a ValidationService with a mock workspace for unit tests."""
    return ValidationService(workspace=MagicMock(spec=Workspace))


def _make_metric(
    metric_id: str = "m1",
    baseline_value: object = None,
    target_value: object = 1.0,
    final_value: object = None,
    status: str | None = None,
) -> ValidationMetric:
    return ValidationMetric(
        metric_id=metric_id,
        baseline_value=baseline_value,
        target_value=target_value,
        final_value=final_value,
        status=status,
    )


def _make_validation(
    metrics: list[ValidationMetric] | None = None,
    scope_ok: bool = True,
    forbidden_violated: bool = False,
    tests_passed: bool = True,
    has_test_results: bool = True,
) -> SubMissionValidation:
    scope = ScopeCheckResult(
        allowed_paths_satisfied=scope_ok,
        forbidden_paths_violated=forbidden_violated,
        violations=[] if scope_ok and not forbidden_violated else ["bad/file.py"],
    )
    test_results = TestResults(
        command="pytest",
        exit_code=0 if tests_passed else 1,
        output="",
        passed=tests_passed,
        duration=0.1,
    ) if has_test_results else None

    return SubMissionValidation(
        sub_mission_id="MF-001-A",
        timestamp=None,
        status="captured",
        deterministic_evidence=DeterministicEvidence(
            files_changed=[],
            scope_check=scope,
            test_results=test_results,
        ),
        metrics=metrics or [],
    )


class TestDetermineMetricStatus:
    def setup_method(self):
        self.svc = _make_service()

    def test_boolean_target_passed(self):
        m = _make_metric(target_value=True, final_value=True)
        assert self.svc._determine_metric_status(m) == "PASSED"

    def test_boolean_target_failed(self):
        m = _make_metric(target_value=True, final_value=False)
        assert self.svc._determine_metric_status(m) == "FAILED"

    def test_string_target_passed(self):
        m = _make_metric(target_value="done", final_value="done")
        assert self.svc._determine_metric_status(m) == "PASSED"

    def test_string_target_failed(self):
        m = _make_metric(target_value="done", final_value="not done")
        assert self.svc._determine_metric_status(m) == "FAILED"

    def test_numeric_improvement_passed(self):
        # target > baseline: need final >= target
        m = _make_metric(baseline_value=0.0, target_value=80.0, final_value=85.0)
        assert self.svc._determine_metric_status(m) == "PASSED"

    def test_numeric_improvement_failed(self):
        m = _make_metric(baseline_value=0.0, target_value=80.0, final_value=70.0)
        assert self.svc._determine_metric_status(m) == "FAILED"

    def test_numeric_reduction_passed(self):
        # target < baseline: need final <= target
        m = _make_metric(baseline_value=100.0, target_value=50.0, final_value=40.0)
        assert self.svc._determine_metric_status(m) == "PASSED"

    def test_numeric_reduction_failed(self):
        m = _make_metric(baseline_value=100.0, target_value=50.0, final_value=60.0)
        assert self.svc._determine_metric_status(m) == "FAILED"

    def test_numeric_maintain_passed(self):
        m = _make_metric(baseline_value=5.0, target_value=5.0, final_value=5.0)
        assert self.svc._determine_metric_status(m) == "PASSED"

    def test_numeric_maintain_failed(self):
        m = _make_metric(baseline_value=5.0, target_value=5.0, final_value=6.0)
        assert self.svc._determine_metric_status(m) == "FAILED"

    def test_numeric_no_baseline_meets_target(self):
        # baseline is None: pass if final >= target
        m = _make_metric(baseline_value=None, target_value=10.0, final_value=10.0)
        assert self.svc._determine_metric_status(m) == "PASSED"

    def test_numeric_no_baseline_exceeds_target(self):
        m = _make_metric(baseline_value=None, target_value=10.0, final_value=15.0)
        assert self.svc._determine_metric_status(m) == "PASSED"

    def test_numeric_no_baseline_below_target(self):
        m = _make_metric(baseline_value=None, target_value=10.0, final_value=5.0)
        assert self.svc._determine_metric_status(m) == "FAILED"


class TestDetermineOverallStatus:
    def setup_method(self):
        self.svc = _make_service()

    def test_all_passed(self):
        m = _make_metric(status="PASSED")
        v = _make_validation(metrics=[m])
        assert self.svc._determine_overall_status(v) == "PASSED"

    def test_metric_failed(self):
        m = _make_metric(status="FAILED")
        v = _make_validation(metrics=[m])
        assert self.svc._determine_overall_status(v) == "FAILED"

    def test_blocked_forbidden_violation(self):
        m = _make_metric(status="PASSED")
        v = _make_validation(metrics=[m], forbidden_violated=True)
        assert self.svc._determine_overall_status(v) == "BLOCKED"

    def test_blocked_out_of_scope(self):
        m = _make_metric(status="PASSED")
        v = _make_validation(metrics=[m], scope_ok=False)
        assert self.svc._determine_overall_status(v) == "BLOCKED"

    def test_blocked_test_failure(self):
        m = _make_metric(status="PASSED")
        v = _make_validation(metrics=[m], tests_passed=False)
        assert self.svc._determine_overall_status(v) == "BLOCKED"

    def test_no_test_results_not_blocked(self):
        m = _make_metric(status="PASSED")
        v = _make_validation(metrics=[m], has_test_results=False)
        assert self.svc._determine_overall_status(v) == "PASSED"

    def test_blocked_takes_priority_over_failed(self):
        m = _make_metric(status="FAILED")
        v = _make_validation(metrics=[m], forbidden_violated=True)
        assert self.svc._determine_overall_status(v) == "BLOCKED"


# Made with Bob
