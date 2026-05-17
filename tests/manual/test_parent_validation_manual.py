#!/usr/bin/env python3
"""Manual test for parent validation CLI command.

This script creates a complete test mission structure and validates
the parent validation command works end-to-end.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import mkdtemp


def create_test_mission_structure(base_dir: Path) -> str:
    """Create a complete test mission structure."""
    mission_id = "TEST-001"
    
    # Create .missionforge structure
    mf_dir = base_dir / ".missionforge"
    missions_dir = mf_dir / "missions"
    missions_dir.mkdir(parents=True)
    
    # Create parent mission
    parent_dir = missions_dir / mission_id
    parent_dir.mkdir()
    
    # Create mission.yaml
    (parent_dir / "mission.yaml").write_text(f"""id: {mission_id}
goal: Test parent validation happy path
description: Manual test for parent validation feature
forbidden_paths:
  - "core/**"
  - "config/**"
sub_missions:
  - TEST-001-A
  - TEST-001-B
  - TEST-001-C
""")
    
    # Create sub-missions directory
    sub_missions_dir = parent_dir / "sub-missions"
    sub_missions_dir.mkdir()
    
    # Create three sub-missions with validation.json
    for sub_id in ["TEST-001-A", "TEST-001-B", "TEST-001-C"]:
        sub_dir = sub_missions_dir / sub_id
        sub_dir.mkdir()
        
        # Create sub-mission.yaml
        (sub_dir / "sub-mission.yaml").write_text(f"""id: {sub_id}
parent: {mission_id}
title: "Test Sub-Mission {sub_id[-1]}"
goal: Test validation workflow
depends_on: []
allowed_paths:
  - "src/api/**"
  - "tests/**"
metrics:
  code_coverage:
    target: 80.0
  complexity:
    target: 10.0
""")
        
        # Create validation.json (simulating successful sub-mission validation)
        validation_data = {
            "sub_mission_id": sub_id,
            "timestamp": "2026-05-17T09:00:00Z",
            "status": "PASSED",
            "deterministic_evidence": {
                "files_changed": [
                    f"src/api/{sub_id.lower()}.py",
                    f"tests/test_{sub_id.lower()}.py"
                ],
                "scope_check": {
                    "allowed_paths_satisfied": True,
                    "forbidden_paths_violated": False,
                    "violations": []
                },
                "test_results": {
                    "command": "pytest tests/",
                    "exit_code": 0,
                    "output": "All tests passed",
                    "passed": True,
                    "duration": 2.5
                }
            },
            "metrics": [
                {
                    "metric_id": "code_coverage",
                    "baseline_value": 65.0,
                    "target_value": 80.0,
                    "final_value": 85.0,
                    "status": "PASSED"
                },
                {
                    "metric_id": "complexity",
                    "baseline_value": 15.0,
                    "target_value": 10.0,
                    "final_value": 8.0,
                    "status": "PASSED"
                }
            ]
        }
        
        with open(sub_dir / "validation.json", "w") as f:
            json.dump(validation_data, f, indent=2)
    
    return mission_id


def run_parent_validation(base_dir: Path, mission_id: str) -> tuple[int, str, str]:
    """Run the parent validation CLI command."""
    cmd = [
        sys.executable, "-m", "missionforge",
        "validate", "parent", mission_id
    ]
    
    result = subprocess.run(
        cmd,
        cwd=base_dir,
        capture_output=True,
        text=True
    )
    
    return result.returncode, result.stdout, result.stderr


def verify_validation_output(base_dir: Path, mission_id: str) -> bool:
    """Verify the validation.json was created correctly."""
    validation_path = base_dir / ".missionforge" / "missions" / mission_id / "validation.json"
    
    if not validation_path.exists():
        print(f"❌ Validation file not found: {validation_path}")
        return False
    
    with open(validation_path) as f:
        data = json.load(f)
    
    # Verify structure
    checks = [
        ("mission_id", data.get("mission_id") == mission_id),
        ("status", data.get("status") == "PASSED"),
        ("timestamp", data.get("timestamp") is not None),
        ("sub_missions.total", data.get("sub_missions", {}).get("total") == 3),
        ("sub_missions.passed", data.get("sub_missions", {}).get("passed") == 3),
        ("sub_missions.failed", data.get("sub_missions", {}).get("failed") == 0),
        ("sub_missions.blocked", data.get("sub_missions", {}).get("blocked") == 0),
        ("forbidden_paths_check", data.get("forbidden_paths_check", {}).get("violated") == False),
    ]
    
    all_passed = True
    for check_name, check_result in checks:
        status = "✓" if check_result else "✗"
        print(f"  {status} {check_name}: {check_result}")
        if not check_result:
            all_passed = False
    
    return all_passed


def main():
    """Run the manual test."""
    print("=" * 70)
    print("PARENT VALIDATION HAPPY PATH TEST")
    print("=" * 70)
    
    # Create temporary directory
    temp_dir = Path(mkdtemp(prefix="mf_test_"))
    print(f"\n📁 Test directory: {temp_dir}")
    
    try:
        # Create test structure
        print("\n1️⃣  Creating test mission structure...")
        mission_id = create_test_mission_structure(temp_dir)
        print(f"   ✓ Created mission {mission_id} with 3 sub-missions")
        
        # Run parent validation
        print(f"\n2️⃣  Running: missionforge validate parent {mission_id}")
        print("-" * 70)
        returncode, stdout, stderr = run_parent_validation(temp_dir, mission_id)
        
        # Display output
        if stdout:
            print(stdout)
        if stderr:
            print("STDERR:", stderr, file=sys.stderr)
        print("-" * 70)
        
        # Check return code
        if returncode != 0:
            print(f"\n❌ Command failed with exit code {returncode}")
            return 1
        
        print(f"\n✓ Command succeeded (exit code: {returncode})")
        
        # Verify output
        print("\n3️⃣  Verifying validation.json...")
        if verify_validation_output(temp_dir, mission_id):
            print("\n✅ ALL CHECKS PASSED")
            print("\n" + "=" * 70)
            print("HAPPY PATH TEST: SUCCESS")
            print("=" * 70)
            return 0
        else:
            print("\n❌ VALIDATION CHECKS FAILED")
            return 1
            
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Cleanup
        print(f"\n🧹 Cleaning up: {temp_dir}")
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
