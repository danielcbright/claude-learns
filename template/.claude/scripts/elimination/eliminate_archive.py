#!/usr/bin/env python3
"""
eliminate_archive.py - Archive a completed elimination session and update learned heuristics

Usage:
    python eliminate_archive.py --outcome success --root-cause "Race condition in cache"
    python eliminate_archive.py --outcome failure --reason "Could not reproduce"
    python eliminate_archive.py --outcome abandoned --reason "User chose different approach"
"""

import argparse
import shutil
import sys
import yaml
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

def update_heuristics(root: Path, session: dict, hypotheses: dict, outcome: str, confirmed_hyp_id: str = None):
    """Update the learned heuristics based on session outcome."""
    heuristics_file = root / ".elimination" / "learned" / "heuristics.yaml"

    # Load existing heuristics
    if heuristics_file.exists():
        with open(heuristics_file, 'r') as f:
            heuristics = yaml.safe_load(f) or {"patterns": [], "statistics": {}}
    else:
        heuristics = {"patterns": [], "statistics": {}}

    # Update global statistics
    stats = heuristics.setdefault("statistics", {})
    stats["total_sessions"] = stats.get("total_sessions", 0) + 1
    stats[f"{outcome}_sessions"] = stats.get(f"{outcome}_sessions", 0) + 1
    stats["total_tests"] = stats.get("total_tests", 0) + session.get("test_count", 0)
    stats["last_updated"] = datetime.now().isoformat()

    # If successful, learn from the confirmed hypothesis
    if outcome == "success" and confirmed_hyp_id:
        confirmed = hypotheses.get(confirmed_hyp_id)
        if confirmed:
            category = confirmed.get("category", "Code")

            # Update category success rates
            cat_stats = stats.setdefault("category_stats", {})
            cat_stat = cat_stats.setdefault(category, {"confirmations": 0, "total": 0})
            cat_stat["confirmations"] += 1
            cat_stat["total"] += 1

            # Check if this matches an existing pattern
            symptom = session.get("symptom", "").lower()
            pattern_matched = False

            for pattern in heuristics.get("patterns", []):
                if pattern.get("category") == category:
                    # Simple keyword matching
                    triggers = pattern.get("trigger_keywords", [])
                    if any(kw.lower() in symptom for kw in triggers):
                        pattern["success_count"] = pattern.get("success_count", 0) + 1
                        pattern["last_matched"] = datetime.now().isoformat()
                        pattern_matched = True
                        break

            # If no pattern matched, consider creating a new one
            # (In a more sophisticated version, we'd use ML to detect patterns)

    # Update category stats for eliminated hypotheses
    for hyp_id, hyp in hypotheses.items():
        if hyp["status"] == "eliminated":
            category = hyp.get("category", "Code")
            cat_stats = stats.setdefault("category_stats", {})
            cat_stat = cat_stats.setdefault(category, {"confirmations": 0, "total": 0})
            cat_stat["total"] += 1

    # Save heuristics
    with open(heuristics_file, 'w') as f:
        yaml.dump(heuristics, f, default_flow_style=False, sort_keys=False)

    return heuristics

def archive_session(root: Path, session: dict, outcome: str, notes: str = None):
    """Move the active session to the archive."""
    # Create archive directory
    archive_base = root / ".elimination" / "archive"
    year_month = datetime.now().strftime("%Y-%m")
    archive_dir = archive_base / year_month / session["session_id"]
    archive_dir.mkdir(parents=True, exist_ok=True)

    # Update session with final info
    session["status"] = "archived"
    session["outcome"] = outcome
    session["archived_at"] = datetime.now().isoformat()
    if notes:
        session["archive_notes"] = notes

    session["process_log"].append({
        "timestamp": datetime.now().isoformat(),
        "action": "session_archived",
        "outcome": outcome,
        "notes": notes
    })

    # Copy files to archive
    active_dir = root / ".elimination" / "active"

    # Save updated session
    with open(archive_dir / "session.yaml", 'w') as f:
        yaml.dump(session, f, default_flow_style=False, sort_keys=False)

    # Copy hypotheses
    hyp_dir = archive_dir / "hypotheses"
    hyp_dir.mkdir(exist_ok=True)
    for hyp_file in (active_dir / "hypotheses").glob("*.yaml"):
        shutil.copy(hyp_file, hyp_dir / hyp_file.name)

    # Copy evidence
    ev_dir = archive_dir / "evidence"
    ev_dir.mkdir(exist_ok=True)
    for ev_file in (active_dir / "evidence").glob("*.yaml"):
        shutil.copy(ev_file, ev_dir / ev_file.name)

    # Clear active session
    for f in (active_dir / "hypotheses").glob("*.yaml"):
        f.unlink()
    for f in (active_dir / "evidence").glob("*.yaml"):
        f.unlink()
    (active_dir / "session.yaml").unlink()

    return archive_dir

def generate_summary(session: dict, hypotheses: dict, outcome: str) -> str:
    """Generate a summary of the session."""
    lines = []
    lines.append(f"# Elimination Session Summary")
    lines.append(f"")
    lines.append(f"**Session**: {session['session_id']}")
    lines.append(f"**Symptom**: {session['symptom']}")
    lines.append(f"**Outcome**: {outcome}")
    lines.append(f"**Duration**: {session.get('created_at', 'N/A')} to {datetime.now().isoformat()}")
    lines.append(f"**Tests run**: {session.get('test_count', 0)}")
    lines.append(f"")

    # Hypothesis summary
    lines.append(f"## Hypotheses")
    lines.append(f"")
    for hid, h in sorted(hypotheses.items(), key=lambda x: x[1]["confidence"], reverse=True):
        status_emoji = {
            "confirmed": "✅",
            "eliminated": "❌",
            "unlikely": "❓",
            "active": "⏳"
        }.get(h["status"], "?")
        lines.append(f"- {status_emoji} **{hid}** ({h['confidence']:.2f}): {h['description']}")

    lines.append(f"")

    # Key learnings
    if outcome == "success":
        confirmed = [h for h in hypotheses.values() if h["status"] == "confirmed"]
        if confirmed:
            lines.append(f"## Root Cause")
            lines.append(f"")
            lines.append(f"{confirmed[0]['description']}")
            lines.append(f"")

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Archive an elimination session")
    parser.add_argument("--outcome", "-o", required=True,
                       choices=["success", "failure", "abandoned"],
                       help="Session outcome")
    parser.add_argument("--root-cause", "-r", help="Description of the root cause (for success)")
    parser.add_argument("--reason", help="Reason for failure/abandonment")
    parser.add_argument("--confirmed", "-c", help="ID of confirmed hypothesis (e.g., H1 or hyp-001)")
    parser.add_argument("--no-learn", action="store_true", help="Skip updating heuristics")

    args = parser.parse_args()

    root = find_project_root()
    if not root:
        print("ERROR: No .elimination directory found.")
        sys.exit(1)

    session = load_session(root)
    if not session:
        print("ERROR: No active session to archive.")
        sys.exit(1)

    hypotheses = load_all_hypotheses(root, session)

    # Determine confirmed hypothesis
    confirmed_hyp_id = None
    if args.confirmed:
        # Normalize ID
        ref = args.confirmed.upper()
        if ref.startswith("H") and ref[1:].isdigit():
            confirmed_hyp_id = f"hyp-{int(ref[1:]):03d}"
        else:
            confirmed_hyp_id = args.confirmed.lower()
    elif args.outcome == "success":
        # Try to find confirmed hypothesis automatically
        confirmed = [hid for hid, h in hypotheses.items() if h["status"] == "confirmed"]
        if confirmed:
            confirmed_hyp_id = confirmed[0]
        else:
            # Use highest confidence
            sorted_hyps = sorted(hypotheses.items(), key=lambda x: x[1]["confidence"], reverse=True)
            if sorted_hyps:
                confirmed_hyp_id = sorted_hyps[0][0]
                print(f"Auto-selected {confirmed_hyp_id} as confirmed (highest confidence)")

    # Build notes
    notes = args.root_cause or args.reason or ""

    print(f"\n{'='*60}")
    print(f"ARCHIVING ELIMINATION SESSION")
    print(f"{'='*60}")
    print(f"\nSession: {session['session_id']}")
    print(f"Outcome: {args.outcome}")
    if confirmed_hyp_id and args.outcome == "success":
        print(f"Confirmed: {confirmed_hyp_id}")
    if notes:
        print(f"Notes: {notes}")

    # Update heuristics
    if not args.no_learn:
        print(f"\nUpdating learned heuristics...")
        heuristics = update_heuristics(root, session, hypotheses, args.outcome, confirmed_hyp_id)
        print(f"  Total sessions: {heuristics['statistics'].get('total_sessions', 0)}")
        print(f"  Success rate: {heuristics['statistics'].get('success_sessions', 0)}/{heuristics['statistics'].get('total_sessions', 0)}")

    # Archive the session
    archive_dir = archive_session(root, session, args.outcome, notes)

    # Generate summary
    summary = generate_summary(session, hypotheses, args.outcome)
    summary_file = archive_dir / "SUMMARY.md"
    with open(summary_file, 'w') as f:
        f.write(summary)

    print(f"\n{'='*60}")
    print(f"SESSION ARCHIVED")
    print(f"{'='*60}")
    print(f"\nArchive location: {archive_dir}")
    print(f"Summary: {summary_file}")
    print(f"\nActive session cleared. Ready for new session.")
    print(f"Run 'python eliminate_init.py' to start a new investigation.")

    # Suggest learning loop
    if args.outcome == "success":
        print(f"\n{'='*60}")
        print(f"RECOMMENDED: Run /learn to capture debugging insights")
        print(f"{'='*60}")
        print(f"\nThis session may have patterns worth remembering:")
        print(f"  - Symptom: {session['symptom']}")
        print(f"  - Root cause category: {hypotheses.get(confirmed_hyp_id, {}).get('category', 'Unknown')}")
        print(f"  - Tests to confirmation: {session.get('test_count', 0)}")

if __name__ == "__main__":
    main()
