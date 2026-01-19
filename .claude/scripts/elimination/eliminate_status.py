#!/usr/bin/env python3
"""
eliminate_status.py - Show current elimination session status and validate process adherence

Usage:
    python eliminate_status.py
    python eliminate_status.py --verbose  # Include confidence history
    python eliminate_status.py --json     # Output as JSON
"""

import argparse
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

def load_hypothesis(root: Path, hyp_id: str) -> dict:
    """Load a hypothesis file."""
    hyp_file = root / ".elimination" / "active" / "hypotheses" / f"{hyp_id}.yaml"
    if not hyp_file.exists():
        return None
    with open(hyp_file, 'r') as f:
        return yaml.safe_load(f)

def load_all_hypotheses(root: Path, session: dict) -> dict:
    """Load all hypotheses into a dict keyed by ID."""
    hypotheses = {}
    for hyp_id in session.get("hypothesis_ids", []):
        hyp = load_hypothesis(root, hyp_id)
        if hyp:
            hypotheses[hyp_id] = hyp
    return hypotheses

def load_evidence(root: Path) -> list:
    """Load all evidence files."""
    evidence_dir = root / ".elimination" / "active" / "evidence"
    evidence = []
    for ev_file in sorted(evidence_dir.glob("*.yaml")):
        with open(ev_file, 'r') as f:
            evidence.append(yaml.safe_load(f))
    return evidence

def validate_process(session: dict, hypotheses: dict, evidence: list) -> list:
    """Validate that the elimination process has been followed correctly."""
    violations = []

    # Check 1: All checkpoints should update all active hypotheses
    for ev in evidence:
        affected = set(ev.get("hypotheses_affected", []))
        # Get hypotheses that were active at that point
        # (This is a simplification - ideally we'd track historical status)
        for hyp_id, hyp in hypotheses.items():
            if hyp["status"] not in ("eliminated",):
                if hyp_id not in affected:
                    # Check if hypothesis was created after this evidence
                    # by comparing timestamps if available
                    pass  # Simplified check

    # Check 2: Confidence changes should be reasonable (not too drastic without explanation)
    for hyp_id, hyp in hypotheses.items():
        history = hyp.get("confidence_history", [])
        for i in range(1, len(history)):
            prev = history[i-1]["confidence"]
            curr = history[i]["confidence"]
            change = abs(curr - prev)
            if change > 0.5:
                violations.append({
                    "type": "LARGE_CONFIDENCE_JUMP",
                    "hypothesis": hyp_id,
                    "change": f"{prev:.2f} -> {curr:.2f}",
                    "severity": "warning"
                })

    # Check 3: Session should not have too many iterations without progress
    if session["current_iteration"] > 10:
        conv = session.get("convergence", {})
        if conv.get("separation_margin", 0) < 0.15:
            violations.append({
                "type": "SLOW_CONVERGENCE",
                "iterations": session["current_iteration"],
                "margin": conv.get("separation_margin", 0),
                "severity": "warning"
            })

    # Check 4: All hypotheses should have been tested at least once after 5 iterations
    if session["current_iteration"] >= 5:
        untested = [hid for hid, h in hypotheses.items()
                   if h["status"] == "active" and len(h.get("evidence_ids", [])) == 0]
        if untested:
            violations.append({
                "type": "UNTESTED_HYPOTHESES",
                "hypotheses": untested,
                "severity": "info"
            })

    return violations

def format_duration(start_str: str) -> str:
    """Format duration from start time to now."""
    try:
        start = datetime.fromisoformat(start_str)
        duration = datetime.now() - start
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        if duration.days > 0:
            return f"{duration.days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    except:
        return "unknown"

def main():
    parser = argparse.ArgumentParser(description="Show elimination session status")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show confidence history")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--validate-only", action="store_true", help="Only run validation checks")

    args = parser.parse_args()

    root = find_project_root()
    if not root:
        if args.json:
            print(json.dumps({"error": "No .elimination directory found"}))
        else:
            print("ERROR: No .elimination directory found.")
            print("Run eliminate_init.py to start a session.")
        sys.exit(1)

    session = load_session(root)
    if not session:
        if args.json:
            print(json.dumps({"error": "No active session"}))
        else:
            print("No active elimination session.")
            print("Run eliminate_init.py to start a session.")
        sys.exit(0)

    hypotheses = load_all_hypotheses(root, session)
    evidence = load_evidence(root)

    # Run validation
    violations = validate_process(session, hypotheses, evidence)

    if args.validate_only:
        if args.json:
            print(json.dumps({"violations": violations}))
        else:
            if violations:
                print("Process Violations Found:")
                for v in violations:
                    print(f"  [{v['severity'].upper()}] {v['type']}: {v}")
            else:
                print("No process violations detected.")
        sys.exit(0 if not violations else 1)

    # Calculate stats
    active_count = sum(1 for h in hypotheses.values() if h["status"] == "active")
    unlikely_count = sum(1 for h in hypotheses.values() if h["status"] == "unlikely")
    eliminated_count = sum(1 for h in hypotheses.values() if h["status"] == "eliminated")
    confirmed_count = sum(1 for h in hypotheses.values() if h["status"] == "confirmed")

    conv = session.get("convergence", {})

    if args.json:
        output = {
            "session": {
                "id": session["session_id"],
                "symptom": session["symptom"],
                "status": session["status"],
                "phase": session["phase"],
                "created_at": session["created_at"],
                "iteration": session["current_iteration"],
                "max_iterations": session["max_iterations"],
                "test_count": session["test_count"]
            },
            "convergence": conv,
            "stats": {
                "active": active_count,
                "unlikely": unlikely_count,
                "eliminated": eliminated_count,
                "confirmed": confirmed_count
            },
            "hypotheses": {
                hid: {
                    "description": h["description"],
                    "category": h["category"],
                    "confidence": h["confidence"],
                    "status": h["status"],
                    "test_count": len(h.get("evidence_ids", []))
                } for hid, h in hypotheses.items()
            },
            "violations": violations
        }
        print(json.dumps(output, indent=2))
        return

    # Pretty print
    print(f"\n{'='*70}")
    print(f"ELIMINATION SESSION STATUS")
    print(f"{'='*70}")

    print(f"\nSession: {session['session_id']}")
    print(f"Symptom: {session['symptom']}")
    print(f"Duration: {format_duration(session['created_at'])}")
    print(f"Phase: {session['phase']}")

    print(f"\n--- Progress ---")
    print(f"Iteration: {session['current_iteration']} / {session['max_iterations']}")
    print(f"Tests run: {session['test_count']}")

    print(f"\n--- Hypothesis Status ---")
    print(f"Active: {active_count} | Unlikely: {unlikely_count} | Eliminated: {eliminated_count} | Confirmed: {confirmed_count}")

    print(f"\n--- Convergence ---")
    if conv.get("is_converged"):
        print(f"STATUS: CONVERGED!")
        print(f"Reason: {conv.get('reason', 'Unknown')}")
    else:
        print(f"STATUS: Not converged")
    print(f"Leading: {conv.get('leading_hypothesis', 'N/A')} ({conv.get('leading_confidence', 0):.2f})")
    print(f"Separation margin: {conv.get('separation_margin', 0):.2f} (need >= 0.30)")

    # Hypothesis table
    print(f"\n{'='*70}")
    print("HYPOTHESES (sorted by confidence)")
    print(f"{'='*70}")
    print(f"{'ID':<10} {'Conf':>6} {'Status':<12} {'Tests':>5} {'Category':<12} Description")
    print("-" * 70)

    sorted_hyps = sorted(hypotheses.items(), key=lambda x: x[1]["confidence"], reverse=True)
    for hid, h in sorted_hyps:
        status_marker = ""
        if h["status"] == "confirmed":
            status_marker = " ***"
        elif h["status"] == "eliminated":
            status_marker = " X"
        elif h["status"] == "unlikely":
            status_marker = " ?"

        print(f"{hid:<10} {h['confidence']:>6.2f} {h['status']:<12} {len(h.get('evidence_ids', [])):>5} {h['category']:<12} {h['description'][:25]}...{status_marker}")

    # Show confidence history if verbose
    if args.verbose:
        print(f"\n{'='*70}")
        print("CONFIDENCE HISTORY")
        print(f"{'='*70}")
        for hid, h in sorted_hyps:
            print(f"\n{hid}: {h['description'][:50]}...")
            for entry in h.get("confidence_history", []):
                print(f"  {entry.get('timestamp', 'N/A')[:19]}: {entry.get('confidence', 0):.2f} - {entry.get('reason', 'N/A')[:40]}")

    # Evidence summary
    if evidence:
        print(f"\n{'='*70}")
        print("EVIDENCE COLLECTED")
        print(f"{'='*70}")
        for ev in evidence[-5:]:  # Show last 5
            print(f"\n{ev['id']}: {ev['test_description'][:50]}...")
            print(f"  Result: {ev['result'][:60]}...")
            print(f"  Updated: {', '.join(ev.get('hypotheses_affected', []))}")

        if len(evidence) > 5:
            print(f"\n... and {len(evidence) - 5} more evidence entries")

    # Violations
    if violations:
        print(f"\n{'='*70}")
        print("PROCESS WARNINGS")
        print(f"{'='*70}")
        for v in violations:
            severity = v["severity"].upper()
            print(f"[{severity}] {v['type']}")
            if "hypothesis" in v:
                print(f"  Hypothesis: {v['hypothesis']}")
            if "change" in v:
                print(f"  Change: {v['change']}")

    # Next action hint
    print(f"\n{'='*70}")
    print("NEXT ACTION")
    print(f"{'='*70}")
    if conv.get("is_converged"):
        print("Session converged. Verify and implement fix.")
        print("  Run: python eliminate_archive.py --outcome success")
    else:
        print("Run: python eliminate_next.py")
        print("  This will tell you exactly which hypothesis to test next.")

if __name__ == "__main__":
    main()
