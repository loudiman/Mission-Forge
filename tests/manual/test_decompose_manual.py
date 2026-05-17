"""Manual test script for decompose command."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd):
    """Run a command and return result."""
    print(f"\n{'=' * 60}")
    print(f"Running: {cmd}")
    print("=" * 60)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    print(f"Exit code: {result.returncode}")
    return result


def main():
    """Test decompose command manually."""

    # Check if we're in the right directory
    if not Path(".missionforge").exists():
        print("ERROR: Not in a MissionForge workspace")
        print("Please run this from a directory with .missionforge/")
        sys.exit(1)

    # Test 1: Show help
    print("\n" + "=" * 60)
    print("TEST 1: Show decompose help")
    print("=" * 60)
    run_command("missionforge decompose --help")

    # Test 2: Show validate-submission help
    print("\n" + "=" * 60)
    print("TEST 2: Show validate-submission help")
    print("=" * 60)
    run_command("missionforge validate-submission --help")

    # Test 3: List available missions
    print("\n" + "=" * 60)
    print("TEST 3: Check available missions")
    print("=" * 60)
    missions_dir = Path(".missionforge/missions")
    if missions_dir.exists():
        missions = [d.name for d in missions_dir.iterdir() if d.is_dir()]
        print(f"Available missions: {missions}")

        if missions:
            test_mission = missions[0]
            print(f"\nTesting with mission: {test_mission}")

            # Test 4: Run decompose
            print("\n" + "=" * 60)
            print(f"TEST 4: Run decompose on {test_mission}")
            print("=" * 60)
            run_command(f"missionforge decompose {test_mission}")

            # Test 5: Check if sub-missions directory was created
            print("\n" + "=" * 60)
            print("TEST 5: Check sub-missions directory")
            print("=" * 60)
            sub_missions_dir = missions_dir / test_mission / "sub-missions"
            if sub_missions_dir.exists():
                print(f"✓ Sub-missions directory created: {sub_missions_dir}")
                sub_files = list(sub_missions_dir.glob("*.yaml"))
                print(f"  Found {len(sub_files)} sub-mission files:")
                for f in sub_files:
                    print(f"    - {f.name}")

                # Test 6: Validate a sub-mission if any exist
                if sub_files:
                    sub_id = sub_files[0].stem
                    print("\n" + "=" * 60)
                    print(f"TEST 6: Validate sub-mission {sub_id}")
                    print("=" * 60)
                    run_command(f"missionforge validate-submission {test_mission} {sub_id}")
            else:
                print(f"✓ Sub-missions directory would be created at: {sub_missions_dir}")
        else:
            print("No missions found. Create one first with: missionforge init MF-001")
    else:
        print("No missions directory found")

    print("\n" + "=" * 60)
    print("MANUAL TESTING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()

# Made with Bob
