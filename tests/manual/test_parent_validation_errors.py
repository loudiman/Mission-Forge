#!/usr/bin/env python3
"""Manual test for parent validation error scenarios.

This script tests various error conditions in the parent validation flow.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import mkdtemp


def create_base_mission(base_dir: Path, mission_id: str = "MF-999") -> Path:
    """Create base mission structure."""
    mf_dir = base_dir / ".missionforge"
    missions_dir = mf_dir / "missions"
    missions_dir.mkdir(parents=True)
    
    parent_dir = missions_dir / mission_id
    parent_dir.mkdir()
    
    (parent_dir / "mission.yaml").write_text(f"""id: {mission_id}
goal: Test error scenarios
forbidden_paths:
  - "core/**"
sub_missions:
  - {mission_id}-A
  - {mission_id}-B
  - {mission_id}-C
""")
    
    sub_missions_dir = parent_dir / "sub-missions"
    sub_missions_dir.mkdir()
    
    return sub_missions_dir


def create_sub_mission_validation(sub_dir: Path, sub_id: str, status: str = "PASSED",
                                  files_changed: list[str] | None = None):
    """Create a sub-mission validation.json."""
    sub_dir.mkdir(exist_ok=True)
    
    if files_changed is None:
        files_changed = [f"src/api/{sub_id.lower()}.py"]
    
    validation_data = {
        "sub_mission_id": sub_id,
        "timestamp": "2026-05-17T09:00:00Z",
        "status": status,
        "deterministic_evidence": {
            "files_changed": files_changed,
            "scope_check": {
                "allowed_paths_satisfied": True,
                "forbidden_paths_violated": False,
                "violations": []
            },
            "test_results": {
                "command": "pytest",
                "exit_code": 0 if status == "PASSED" else 1,
                "output": "Tests passed" if status == "PASSED" else "Tests failed",
                "passed": status == "PASSED",
                "duration": 1.0
            }
        },
        "metrics": []
    }
    
    with open(sub_dir / "validation.json", "w") as f:
        json.dump(validation_data, f, indent=2)


def run_validation(base_dir: Path, mission_id: str) -> tuple[int, str, str]:
    """Run parent validation command."""
    cmd = [sys.executable, "-m", "missionforge", "validate", "parent", mission_id]
    result = subprocess.run(cmd, cwd=base_dir, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def test_missing_sub_mission_validation():
    """Test error when sub-mission validation.json is missing."""
    print("\n" + "=" * 70)
    print("TEST 1: Missing Sub-Mission Validation")
    print("=" * 70)
    
    temp_dir = Path(mkdtemp(prefix="mf_err1_"))
    try:
        mission_id = "MF-999"
        sub_dir = create_base_mission(temp_dir, mission_id)
        
        # Create only 2 out of 3 sub-missions
        create_sub_mission_validation(sub_dir / f"{mission_id}-A", f"{mission_id}-A")
        create_sub_mission_validation(sub_dir / f"{mission_id}-B", f"{mission_id}-B")
        # Missing: TEST-ERR-C
        
        print(f"📁 Created mission with 2/3 sub-missions validated")
        print(f"🔍 Running validation (should fail)...")
        
        returncode, stdout, stderr = run_validation(temp_dir, mission_id)
        
        print(stdout)
        if stderr:
            print("STDERR:", stderr)
        
        if returncode != 0 and "missing validation.json" in stdout.lower():
            print("✅ PASS: Correctly detected missing validation")
            return True
        else:
            print(f"❌ FAIL: Expected error but got exit code {returncode}")
            return False
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_sub_mission_failed():
    """Test error when sub-mission has FAILED status."""
    print("\n" + "=" * 70)
    print("TEST 2: Sub-Mission Failed")
    print("=" * 70)
    
    temp_dir = Path(mkdtemp(prefix="mf_err2_"))
    try:
        mission_id = "MF-999"
        sub_dir = create_base_mission(temp_dir, mission_id)
        
        # Create 3 sub-missions, one with FAILED status
        create_sub_mission_validation(sub_dir / f"{mission_id}-A", f"{mission_id}-A", "PASSED")
        create_sub_mission_validation(sub_dir / f"{mission_id}-B", f"{mission_id}-B", "FAILED")
        create_sub_mission_validation(sub_dir / f"{mission_id}-C", f"{mission_id}-C", "PASSED")
        
        print(f"📁 Created mission with 1 FAILED sub-mission")
        print(f"🔍 Running validation (should fail)...")
        
        returncode, stdout, stderr = run_validation(temp_dir, mission_id)
        
        print(stdout)
        if stderr:
            print("STDERR:", stderr)
        
        if returncode != 0 and "failed" in stdout.lower():
            print("✅ PASS: Correctly detected failed sub-mission")
            return True
        else:
            print(f"❌ FAIL: Expected error but got exit code {returncode}")
            return False
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_forbidden_paths_violation():
    """Test error when forbidden paths are violated."""
    print("\n" + "=" * 70)
    print("TEST 3: Forbidden Paths Violation")
    print("=" * 70)
    
    temp_dir = Path(mkdtemp(prefix="mf_err3_"))
    try:
        mission_id = "MF-999"
        sub_dir = create_base_mission(temp_dir, mission_id)
        
        # Create sub-missions with one violating forbidden paths
        create_sub_mission_validation(
            sub_dir / f"{mission_id}-A", 
            f"{mission_id}-A", 
            "PASSED",
            files_changed=["core/critical.py"]  # Violates forbidden_paths
        )
        create_sub_mission_validation(sub_dir / f"{mission_id}-B", f"{mission_id}-B", "PASSED")
        create_sub_mission_validation(sub_dir / f"{mission_id}-C", f"{mission_id}-C", "PASSED")
        
        print(f"📁 Created mission with forbidden path violation")
        print(f"🔍 Running validation (should fail)...")
        
        returncode, stdout, stderr = run_validation(temp_dir, mission_id)
        
        print(stdout)
        if stderr:
            print("STDERR:", stderr)
        
        if returncode != 0 and "forbidden" in stdout.lower():
            print("✅ PASS: Correctly detected forbidden paths violation")
            return True
        else:
            print(f"❌ FAIL: Expected error but got exit code {returncode}")
            return False
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_blocked_sub_mission():
    """Test error when sub-mission has BLOCKED status."""
    print("\n" + "=" * 70)
    print("TEST 4: Sub-Mission Blocked")
    print("=" * 70)
    
    temp_dir = Path(mkdtemp(prefix="mf_err4_"))
    try:
        mission_id = "MF-999"
        sub_dir = create_base_mission(temp_dir, mission_id)
        
        # Create 3 sub-missions, one with BLOCKED status
        create_sub_mission_validation(sub_dir / f"{mission_id}-A", f"{mission_id}-A", "PASSED")
        create_sub_mission_validation(sub_dir / f"{mission_id}-B", f"{mission_id}-B", "BLOCKED")
        create_sub_mission_validation(sub_dir / f"{mission_id}-C", f"{mission_id}-C", "PASSED")
        
        print(f"📁 Created mission with 1 BLOCKED sub-mission")
        print(f"🔍 Running validation (should fail)...")
        
        returncode, stdout, stderr = run_validation(temp_dir, mission_id)
        
        print(stdout)
        if stderr:
            print("STDERR:", stderr)
        
        if returncode != 0 and "blocked" in stdout.lower():
            print("✅ PASS: Correctly detected blocked sub-mission")
            return True
        else:
            print(f"❌ FAIL: Expected error but got exit code {returncode}")
            return False
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    """Run all error scenario tests."""
    print("=" * 70)
    print("PARENT VALIDATION ERROR SCENARIOS TEST")
    print("=" * 70)
    
    tests = [
        test_missing_sub_mission_validation,
        test_sub_mission_failed,
        test_forbidden_paths_violation,
        test_blocked_sub_mission,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"\n❌ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ ALL ERROR SCENARIO TESTS PASSED")
        return 0
    else:
        print(f"\n❌ {total - passed} TEST(S) FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
