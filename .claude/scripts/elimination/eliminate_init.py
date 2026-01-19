#!/usr/bin/env python3
"""
eliminate_init.py - Initialize an elimination debugging session

Usage:
    python eliminate_init.py --symptom "API returning 500 errors" --hypotheses hypotheses.yaml
    python eliminate_init.py --symptom "Login fails intermittently" --interactive

Creates:
    .elimination/active/session.yaml
    .elimination/active/hypotheses/hyp-001.yaml, hyp-002.yaml, ...
    .elimination/active/evidence/  (empty directory)
"""

import argparse
import os
import sys
import yaml
from datetime import datetime
from pathlib import Path

# Default confidence priors by category
DEFAULT_PRIORS = {
    "Code": 0.35,
    "Config": 0.20,
    "Dependencies": 0.15,
    "Data": 0.15,
    "Infrastructure": 0.10,
    "Concurrency": 0.05,
}

def find_project_root():
    """Find the project root by looking for .elimination or .git directory."""
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / ".elimination").exists() or (parent / ".git").exists():
            return parent
    return current

def ensure_directory_structure(root: Path):
    """Create the elimination directory structure if it doesn't exist."""
    dirs = [
        root / ".elimination" / "active" / "hypotheses",
        root / ".elimination" / "active" / "evidence",
        root / ".elimination" / "logs",
        root / ".elimination" / "learned" / "templates",
        root / ".elimination" / "archive",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

def check_active_session(root: Path) -> bool:
    """Check if there's already an active session."""
    session_file = root / ".elimination" / "active" / "session.yaml"
    return session_file.exists()

def load_hypotheses_from_file(filepath: str) -> list:
    """Load hypotheses from a YAML file."""
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)
    return data.get('hypotheses', [])

def create_hypothesis_file(root: Path, hyp_id: str, hypothesis: dict):
    """Create a hypothesis YAML file."""
    hyp_file = root / ".elimination" / "active" / "hypotheses" / f"{hyp_id}.yaml"

    # Ensure required fields
    hyp_data = {
        "id": hyp_id,
        "description": hypothesis.get("description", ""),
        "category": hypothesis.get("category", "Code"),
        "confidence": hypothesis.get("confidence", DEFAULT_PRIORS.get(hypothesis.get("category", "Code"), 0.30)),
        "initial_confidence": hypothesis.get("confidence", DEFAULT_PRIORS.get(hypothesis.get("category", "Code"), 0.30)),
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "evidence_ids": [],
        "confidence_history": [
            {
                "timestamp": datetime.now().isoformat(),
                "confidence": hypothesis.get("confidence", DEFAULT_PRIORS.get(hypothesis.get("category", "Code"), 0.30)),
                "reason": "Initial assignment"
            }
        ],
        "rollback_info": {
            "can_resurrect": True,
            "elimination_evidence": None
        }
    }

    with open(hyp_file, 'w') as f:
        yaml.dump(hyp_data, f, default_flow_style=False, sort_keys=False)

    return hyp_data

def create_session_file(root: Path, symptom: str, hypotheses: list, spec_reference: str = None):
    """Create the session.yaml file."""
    session_file = root / ".elimination" / "active" / "session.yaml"

    session_data = {
        "session_id": datetime.now().strftime("session-%Y%m%d-%H%M%S"),
        "created_at": datetime.now().isoformat(),
        "symptom": symptom,
        "status": "active",
        "phase": "evidence_gathering",
        "spec_reference": spec_reference,
        "session_type": "spec_deviation_debug" if spec_reference else "standard",
        "hypothesis_count": len(hypotheses),
        "test_count": 0,
        "current_iteration": 0,
        "max_iterations": 20,
        "convergence": {
            "leading_hypothesis": None,
            "leading_confidence": 0.0,
            "separation_margin": 0.0,
            "is_converged": False
        },
        "hypothesis_ids": [f"hyp-{i+1:03d}" for i in range(len(hypotheses))],
        "process_log": [
            {
                "timestamp": datetime.now().isoformat(),
                "action": "session_initialized",
                "details": f"Created session with {len(hypotheses)} hypotheses"
            }
        ]
    }

    with open(session_file, 'w') as f:
        yaml.dump(session_data, f, default_flow_style=False, sort_keys=False)

    return session_data

def interactive_hypothesis_entry() -> list:
    """Interactively collect hypotheses from the user."""
    print("\n=== Interactive Hypothesis Entry ===")
    print("Enter hypotheses one at a time. Type 'done' when finished.\n")
    print("Categories: Code, Config, Dependencies, Data, Infrastructure, Concurrency\n")

    hypotheses = []
    idx = 1

    while True:
        print(f"--- Hypothesis {idx} ---")
        desc = input("Description (or 'done'): ").strip()

        if desc.lower() == 'done':
            if not hypotheses:
                print("Error: At least one hypothesis is required.")
                continue
            break

        category = input(f"Category [{', '.join(DEFAULT_PRIORS.keys())}]: ").strip()
        if category not in DEFAULT_PRIORS:
            print(f"  Using default category 'Code'")
            category = "Code"

        confidence_str = input(f"Initial confidence (default {DEFAULT_PRIORS[category]}): ").strip()
        try:
            confidence = float(confidence_str) if confidence_str else DEFAULT_PRIORS[category]
        except ValueError:
            confidence = DEFAULT_PRIORS[category]

        hypotheses.append({
            "description": desc,
            "category": category,
            "confidence": confidence
        })

        print(f"  Added: {desc} ({category}, {confidence})\n")
        idx += 1

    return hypotheses

def main():
    parser = argparse.ArgumentParser(description="Initialize an elimination debugging session")
    parser.add_argument("--symptom", "-s", required=True, help="Description of the symptom being debugged")
    parser.add_argument("--hypotheses", "-h", dest="hyp_file", help="YAML file containing hypotheses")
    parser.add_argument("--interactive", "-i", action="store_true", help="Enter hypotheses interactively")
    parser.add_argument("--spec", help="Reference to a spec file if debugging a specced feature")
    parser.add_argument("--force", "-f", action="store_true", help="Force overwrite existing session")
    parser.add_argument("--json-hypotheses", "-j", help="JSON string of hypotheses for programmatic use")

    args = parser.parse_args()

    root = find_project_root()
    ensure_directory_structure(root)

    # Check for existing session
    if check_active_session(root) and not args.force:
        print("ERROR: An active session already exists.")
        print("Use --force to overwrite, or run eliminate_archive.py first.")
        print(f"Session file: {root / '.elimination' / 'active' / 'session.yaml'}")
        sys.exit(1)

    # Clear existing active session if forcing
    if args.force:
        active_dir = root / ".elimination" / "active"
        for f in (active_dir / "hypotheses").glob("*.yaml"):
            f.unlink()
        for f in (active_dir / "evidence").glob("*.yaml"):
            f.unlink()
        session_file = active_dir / "session.yaml"
        if session_file.exists():
            session_file.unlink()

    # Get hypotheses
    hypotheses = []

    if args.json_hypotheses:
        import json
        hypotheses = json.loads(args.json_hypotheses)
    elif args.hyp_file:
        hypotheses = load_hypotheses_from_file(args.hyp_file)
    elif args.interactive:
        hypotheses = interactive_hypothesis_entry()
    else:
        print("ERROR: Must provide --hypotheses, --json-hypotheses, or --interactive")
        sys.exit(1)

    if not hypotheses:
        print("ERROR: No hypotheses provided")
        sys.exit(1)

    # Sort hypotheses by confidence (descending) for initial ranking
    hypotheses.sort(key=lambda h: h.get("confidence", 0.30), reverse=True)

    # Create hypothesis files
    print(f"\nInitializing elimination session for: {args.symptom}")
    print(f"Project root: {root}")
    print(f"\nCreating {len(hypotheses)} hypotheses:")

    for i, hyp in enumerate(hypotheses):
        hyp_id = f"hyp-{i+1:03d}"
        hyp_data = create_hypothesis_file(root, hyp_id, hyp)
        print(f"  {hyp_id}: {hyp_data['description'][:50]}... ({hyp_data['category']}, {hyp_data['confidence']:.2f})")

    # Create session file
    session_data = create_session_file(root, args.symptom, hypotheses, args.spec)

    print(f"\n{'='*60}")
    print(f"Session initialized: {session_data['session_id']}")
    print(f"{'='*60}")
    print(f"\nNext steps:")
    print(f"  1. Run: python eliminate_next.py")
    print(f"     This will tell you which hypothesis to test first.")
    print(f"  2. After testing, run: python eliminate_checkpoint.py --test '...' --evidence '...'")
    print(f"  3. Repeat until convergence.")
    print(f"\nRun 'python eliminate_status.py' at any time to see current state.")

if __name__ == "__main__":
    main()
