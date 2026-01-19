#!/usr/bin/env python3
"""
eliminate_checkpoint.py - Record a test and update hypothesis confidences

CRITICAL: This script ENFORCES process adherence by:
1. Requiring ALL hypotheses to have updated confidences
2. Validating confidence changes are reasonable
3. Logging the checkpoint to the process log
4. Determining next action automatically

Usage:
    python eliminate_checkpoint.py --test "Check DB connections" --evidence "Pool at 45%" --updates "H1:0.15,H2:0.42,H3:0.38"
    python eliminate_checkpoint.py --test "Memory check" --evidence "Stable" --updates-file updates.yaml
"""

import argparse
import os
import sys
import yaml
import json
from datetime import datetime
from pathlib import Path

def find_project_root():
    """Find the project root by looking for .elimination directory."""
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / ".elimination").exists():
            return parent
    return None

def load_session(root: Path) -> dict:
    """Load the current session."""
    session_file = root / ".elimination" / "active" / "session.yaml"
    if not session_file.exists():
        return None
    with open(session_file, 'r') as f:
        return yaml.safe_load(f)

def save_session(root: Path, session: dict):
    """Save the session."""
    session_file = root / ".elimination" / "active" / "session.yaml"
    with open(session_file, 'w') as f:
        yaml.dump(session, f, default_flow_style=False, sort_keys=False)

def load_hypothesis(root: Path, hyp_id: str) -> dict:
    """Load a hypothesis file."""
    hyp_file = root / ".elimination" / "active" / "hypotheses" / f"{hyp_id}.yaml"
    if not hyp_file.exists():
        return None
    with open(hyp_file, 'r') as f:
        return yaml.safe_load(f)

def save_hypothesis(root: Path, hyp_id: str, hyp: dict):
    """Save a hypothesis file."""
    hyp_file = root / ".elimination" / "active" / "hypotheses" / f"{hyp_id}.yaml"
    with open(hyp_file, 'w') as f:
        yaml.dump(hyp, f, default_flow_style=False, sort_keys=False)

def load_all_hypotheses(root: Path, session: dict) -> dict:
    """Load all hypotheses into a dict keyed by ID."""
    hypotheses = {}
    for hyp_id in session.get("hypothesis_ids", []):
        hyp = load_hypothesis(root, hyp_id)
        if hyp:
            hypotheses[hyp_id] = hyp
    return hypotheses

def parse_updates(updates_str: str) -> dict:
    """Parse updates string like 'H1:0.15,H2:0.42,H3:0.38' into dict."""
    updates = {}
    for part in updates_str.split(","):
        part = part.strip()
        if ":" not in part:
            continue
        hyp_ref, conf_str = part.split(":", 1)
        # Normalize hypothesis reference (H1 -> hyp-001, hyp-001 -> hyp-001)
        hyp_ref = hyp_ref.strip().upper()
        if hyp_ref.startswith("H") and hyp_ref[1:].isdigit():
            hyp_id = f"hyp-{int(hyp_ref[1:]):03d}"
        elif hyp_ref.startswith("HYP-"):
            hyp_id = hyp_ref.lower()
        else:
            hyp_id = hyp_ref.lower()

        try:
            # Handle "0.70->0.15" format or just "0.15"
            if "->" in conf_str:
                conf_str = conf_str.split("->")[1]
            confidence = float(conf_str.strip())
            updates[hyp_id] = confidence
        except ValueError:
            print(f"Warning: Could not parse confidence for {hyp_ref}: {conf_str}")

    return updates

def determine_status(confidence: float) -> str:
    """Determine hypothesis status based on confidence."""
    if confidence >= 0.90:
        return "confirmed"
    elif confidence < 0.05:
        return "eliminated"
    elif confidence < 0.25:
        return "unlikely"
    else:
        return "active"

def check_convergence(hypotheses: dict) -> dict:
    """Check if the session has converged."""
    # Get active/unlikely hypotheses sorted by confidence
    active_hyps = [(hid, h) for hid, h in hypotheses.items() if h["status"] in ("active", "unlikely", "confirmed")]
    if not active_hyps:
        return {"is_converged": False, "reason": "No active hypotheses"}

    active_hyps.sort(key=lambda x: x[1]["confidence"], reverse=True)

    leading_id, leading = active_hyps[0]
    leading_confidence = leading["confidence"]

    # Check for confirmation
    if leading["status"] == "confirmed" or leading_confidence >= 0.90:
        return {
            "is_converged": True,
            "reason": "Leading hypothesis confirmed (confidence >= 0.90)",
            "leading_hypothesis": leading_id,
            "leading_confidence": leading_confidence,
            "separation_margin": leading_confidence - (active_hyps[1][1]["confidence"] if len(active_hyps) > 1 else 0)
        }

    # Check separation margin
    if len(active_hyps) > 1:
        second_confidence = active_hyps[1][1]["confidence"]
        margin = leading_confidence - second_confidence
        if margin >= 0.30:
            return {
                "is_converged": True,
                "reason": f"Separation margin >= 0.30 ({margin:.2f})",
                "leading_hypothesis": leading_id,
                "leading_confidence": leading_confidence,
                "separation_margin": margin
            }
    else:
        margin = leading_confidence

    return {
        "is_converged": False,
        "leading_hypothesis": leading_id,
        "leading_confidence": leading_confidence,
        "separation_margin": margin if len(active_hyps) > 1 else leading_confidence
    }

def create_evidence_file(root: Path, session: dict, test: str, evidence: str, updates: dict) -> str:
    """Create an evidence file."""
    evidence_dir = root / ".elimination" / "active" / "evidence"
    evidence_id = f"ev-{session['test_count'] + 1:03d}"
    evidence_file = evidence_dir / f"{evidence_id}.yaml"

    evidence_data = {
        "id": evidence_id,
        "test_description": test,
        "result": evidence,
        "timestamp": datetime.now().isoformat(),
        "iteration": session["current_iteration"] + 1,
        "confidence_updates": {k: v for k, v in updates.items()},
        "hypotheses_affected": list(updates.keys())
    }

    with open(evidence_file, 'w') as f:
        yaml.dump(evidence_data, f, default_flow_style=False, sort_keys=False)

    return evidence_id

def main():
    parser = argparse.ArgumentParser(description="Record a test checkpoint in elimination debugging")
    parser.add_argument("--test", "-t", required=True, help="Description of the test performed")
    parser.add_argument("--evidence", "-e", required=True, help="What was observed/evidence collected")
    parser.add_argument("--updates", "-u", help="Confidence updates: 'H1:0.15,H2:0.42,H3:0.38'")
    parser.add_argument("--updates-file", help="YAML file with confidence updates")
    parser.add_argument("--skip-validation", action="store_true", help="Skip validation (not recommended)")

    args = parser.parse_args()

    root = find_project_root()
    if not root:
        print("ERROR: No .elimination directory found. Run eliminate_init.py first.")
        sys.exit(1)

    session = load_session(root)
    if not session:
        print("ERROR: No active session found. Run eliminate_init.py first.")
        sys.exit(1)

    # Load all hypotheses
    hypotheses = load_all_hypotheses(root, session)
    if not hypotheses:
        print("ERROR: No hypotheses found in session.")
        sys.exit(1)

    # Parse updates
    if args.updates:
        updates = parse_updates(args.updates)
    elif args.updates_file:
        with open(args.updates_file, 'r') as f:
            updates = yaml.safe_load(f)
    else:
        print("ERROR: Must provide --updates or --updates-file")
        sys.exit(1)

    # CRITICAL VALIDATION: All hypotheses must have updates
    if not args.skip_validation:
        missing_updates = []
        for hyp_id, hyp in hypotheses.items():
            if hyp["status"] not in ("eliminated",) and hyp_id not in updates:
                missing_updates.append(hyp_id)

        if missing_updates:
            print("=" * 60)
            print("ERROR: PROCESS VIOLATION - Missing confidence updates!")
            print("=" * 60)
            print("\nYou must update ALL active hypotheses after each test.")
            print("Evidence often affects multiple hypotheses.\n")
            print("Missing updates for:")
            for hyp_id in missing_updates:
                hyp = hypotheses[hyp_id]
                print(f"  - {hyp_id}: {hyp['description'][:50]}... (current: {hyp['confidence']:.2f})")
            print("\nIf a hypothesis is truly unaffected, provide its current confidence.")
            print("Example: --updates 'H1:0.15,H2:0.42,H3:0.35'")
            print("\nUse --skip-validation to bypass (not recommended).")
            sys.exit(1)

    # Validate confidence values
    for hyp_id, new_conf in updates.items():
        if not (0.0 <= new_conf <= 1.0):
            print(f"ERROR: Invalid confidence for {hyp_id}: {new_conf} (must be 0.0-1.0)")
            sys.exit(1)

    # Create evidence file
    evidence_id = create_evidence_file(root, session, args.test, args.evidence, updates)

    # Update hypotheses
    print(f"\n{'='*60}")
    print(f"Checkpoint: Test #{session['test_count'] + 1}")
    print(f"{'='*60}")
    print(f"\nTest: {args.test}")
    print(f"Evidence: {args.evidence}")
    print(f"\nHypothesis Updates:")
    print(f"{'ID':<10} {'Description':<35} {'Previous':>10} {'New':>10} {'Status':<12}")
    print("-" * 80)

    status_changes = []
    for hyp_id, hyp in hypotheses.items():
        if hyp_id in updates:
            old_conf = hyp["confidence"]
            new_conf = updates[hyp_id]
            old_status = hyp["status"]
            new_status = determine_status(new_conf)

            # Update hypothesis
            hyp["confidence"] = new_conf
            hyp["status"] = new_status
            hyp["evidence_ids"].append(evidence_id)
            hyp["confidence_history"].append({
                "timestamp": datetime.now().isoformat(),
                "confidence": new_conf,
                "reason": f"Test: {args.test[:30]}...",
                "evidence_id": evidence_id
            })

            if new_status == "eliminated":
                hyp["rollback_info"]["elimination_evidence"] = evidence_id

            save_hypothesis(root, hyp_id, hyp)

            # Format output
            status_marker = ""
            if new_status != old_status:
                status_marker = f" <- {new_status.upper()}"
                status_changes.append((hyp_id, old_status, new_status))

            desc = hyp["description"][:35]
            print(f"{hyp_id:<10} {desc:<35} {old_conf:>10.2f} {new_conf:>10.2f} {new_status:<12}{status_marker}")

    # Update session
    session["test_count"] += 1
    session["current_iteration"] += 1

    # Check convergence
    hypotheses = load_all_hypotheses(root, session)  # Reload with updates
    convergence = check_convergence(hypotheses)
    session["convergence"] = convergence

    # Log to process log
    session["process_log"].append({
        "timestamp": datetime.now().isoformat(),
        "action": "checkpoint",
        "test": args.test,
        "evidence_id": evidence_id,
        "updates_count": len(updates),
        "convergence_status": convergence["is_converged"]
    })

    save_session(root, session)

    # Print convergence status
    print(f"\n{'='*60}")
    print("Convergence Check")
    print(f"{'='*60}")
    print(f"Leading hypothesis: {convergence.get('leading_hypothesis', 'N/A')}")
    print(f"Leading confidence: {convergence.get('leading_confidence', 0):.2f}")
    print(f"Separation margin:  {convergence.get('separation_margin', 0):.2f} (need >= 0.30)")
    print(f"Status: {'CONVERGED' if convergence['is_converged'] else 'NOT CONVERGED'}")

    if convergence["is_converged"]:
        print(f"\n{'='*60}")
        print("SESSION CONVERGED!")
        print(f"{'='*60}")
        print(f"Reason: {convergence.get('reason', 'Unknown')}")
        print(f"\nNext steps:")
        print(f"  1. Verify the hypothesis: {convergence['leading_hypothesis']}")
        print(f"  2. Implement the fix")
        print(f"  3. Run: python eliminate_archive.py --outcome success")
    else:
        # Determine next action
        print(f"\n{'='*60}")
        print("Next Action")
        print(f"{'='*60}")
        # Find highest confidence active hypothesis
        active_hyps = [(hid, h) for hid, h in hypotheses.items() if h["status"] == "active"]
        active_hyps.sort(key=lambda x: x[1]["confidence"], reverse=True)

        if active_hyps:
            next_hyp_id, next_hyp = active_hyps[0]
            print(f"Test hypothesis: {next_hyp_id}")
            print(f"Description: {next_hyp['description']}")
            print(f"Current confidence: {next_hyp['confidence']:.2f}")
            print(f"\nDesign a test that would ELIMINATE this hypothesis if the result is negative.")
        else:
            print("WARNING: No active hypotheses remaining!")
            print("Consider:")
            print("  1. Resurrecting eliminated hypotheses")
            print("  2. Adding new hypotheses via eliminate_init.py --force")

    # Log to elimination log
    log_file = root / ".elimination" / "logs" / "elimination_log.yaml"
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "session_id": session["session_id"],
        "test_number": session["test_count"],
        "evidence_id": evidence_id,
        "status_changes": status_changes,
        "convergence": convergence["is_converged"]
    }

    if log_file.exists():
        with open(log_file, 'r') as f:
            log_data = yaml.safe_load(f) or {"entries": []}
    else:
        log_data = {"entries": []}

    log_data["entries"].append(log_entry)

    with open(log_file, 'w') as f:
        yaml.dump(log_data, f, default_flow_style=False, sort_keys=False)

    print(f"\nEvidence recorded: {evidence_id}")
    print(f"Run 'python eliminate_status.py' for full session status.")

if __name__ == "__main__":
    main()
