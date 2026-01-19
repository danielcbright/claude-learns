#!/usr/bin/env python3
"""
eliminate_next.py - Determine the next action in elimination debugging

This script removes Claude's discretion about what to test next.
It returns the EXACT hypothesis that should be tested, based on:
1. Highest confidence among active hypotheses
2. Expected information gain
3. Process state

Usage:
    python eliminate_next.py
    python eliminate_next.py --json  # Output as JSON for programmatic use
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

def calculate_information_gain(hyp: dict) -> float:
    """
    Calculate expected information gain from testing this hypothesis.

    Information gain is higher when:
    - Confidence is closer to 0.5 (maximum uncertainty)
    - The hypothesis could affect other hypotheses
    - The hypothesis hasn't been tested much yet
    """
    conf = hyp["confidence"]

    # Shannon entropy-based information gain (max at 0.5)
    # Using a simplified approximation
    entropy = 1 - abs(2 * conf - 1)  # 0 at 0 or 1, 1 at 0.5

    # Boost for less-tested hypotheses
    test_count = len(hyp.get("evidence_ids", []))
    freshness_bonus = 1.0 / (1 + test_count * 0.2)

    # Combine factors
    return entropy * 0.7 + freshness_bonus * 0.3

def get_next_hypothesis(hypotheses: dict) -> tuple:
    """
    Determine which hypothesis to test next.

    Returns: (hyp_id, hyp_data, reason)
    """
    # Filter to active hypotheses only
    active_hyps = [(hid, h) for hid, h in hypotheses.items() if h["status"] == "active"]

    if not active_hyps:
        # Check if there are unlikely hypotheses we might resurrect
        unlikely_hyps = [(hid, h) for hid, h in hypotheses.items() if h["status"] == "unlikely"]
        if unlikely_hyps:
            return None, None, "NO_ACTIVE_HYPOTHESES_UNLIKELY_REMAIN"
        return None, None, "NO_HYPOTHESES_REMAINING"

    # Sort by confidence (descending) - test highest confidence first
    # This is the standard approach: try to confirm the most likely hypothesis
    active_hyps.sort(key=lambda x: x[1]["confidence"], reverse=True)

    # However, if confidences are close, prefer higher information gain
    top_conf = active_hyps[0][1]["confidence"]

    # Get hypotheses within 0.10 of the top confidence
    close_hyps = [(hid, h) for hid, h in active_hyps if top_conf - h["confidence"] <= 0.10]

    if len(close_hyps) > 1:
        # Multiple hypotheses with similar confidence - use information gain
        close_hyps.sort(key=lambda x: calculate_information_gain(x[1]), reverse=True)
        next_id, next_hyp = close_hyps[0]
        reason = f"HIGHEST_INFO_GAIN_AMONG_TOP_{len(close_hyps)}"
    else:
        next_id, next_hyp = active_hyps[0]
        reason = "HIGHEST_CONFIDENCE"

    return next_id, next_hyp, reason

def suggest_test(hyp: dict) -> str:
    """Suggest a test based on hypothesis category."""
    category = hyp.get("category", "Code")

    suggestions = {
        "Code": "Review the relevant code paths, add logging, or write a targeted unit test",
        "Config": "Check configuration values, environment variables, and feature flags",
        "Dependencies": "Verify dependency versions, check for breaking changes in changelogs",
        "Data": "Inspect the data at the point of failure, check for edge cases or corruption",
        "Infrastructure": "Check resource metrics (CPU, memory, disk), service health, and network connectivity",
        "Concurrency": "Add mutex logging, check for race conditions with concurrent request testing"
    }

    return suggestions.get(category, "Design a test that would eliminate this hypothesis if negative")

def main():
    parser = argparse.ArgumentParser(description="Determine next action in elimination debugging")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    root = find_project_root()
    if not root:
        if args.json:
            print(json.dumps({"error": "No .elimination directory found"}))
        else:
            print("ERROR: No .elimination directory found. Run eliminate_init.py first.")
        sys.exit(1)

    session = load_session(root)
    if not session:
        if args.json:
            print(json.dumps({"error": "No active session"}))
        else:
            print("ERROR: No active session found. Run eliminate_init.py first.")
        sys.exit(1)

    # Check convergence first
    if session.get("convergence", {}).get("is_converged", False):
        conv = session["convergence"]
        if args.json:
            print(json.dumps({
                "status": "CONVERGED",
                "leading_hypothesis": conv["leading_hypothesis"],
                "confidence": conv["leading_confidence"],
                "action": "VERIFY_AND_FIX"
            }))
        else:
            print(f"{'='*60}")
            print("SESSION CONVERGED")
            print(f"{'='*60}")
            print(f"\nLeading hypothesis: {conv['leading_hypothesis']}")
            print(f"Confidence: {conv['leading_confidence']:.2f}")
            print(f"\nNext action: VERIFY AND IMPLEMENT FIX")
            print(f"\nSteps:")
            print(f"  1. Implement the fix based on {conv['leading_hypothesis']}")
            print(f"  2. Verify the fix resolves the symptom")
            print(f"  3. Run: python eliminate_archive.py --outcome success")
        sys.exit(0)

    # Check iteration limit
    if session["current_iteration"] >= session["max_iterations"]:
        if args.json:
            print(json.dumps({
                "status": "MAX_ITERATIONS_REACHED",
                "iterations": session["current_iteration"],
                "action": "REVIEW_OR_EXPAND"
            }))
        else:
            print(f"{'='*60}")
            print("MAXIMUM ITERATIONS REACHED")
            print(f"{'='*60}")
            print(f"\nIterations: {session['current_iteration']} / {session['max_iterations']}")
            print(f"\nOptions:")
            print(f"  1. Review eliminated hypotheses for resurrection")
            print(f"  2. Expand hypothesis space with new ideas")
            print(f"  3. Increase max_iterations in session.yaml")
        sys.exit(0)

    # Load hypotheses and determine next
    hypotheses = load_all_hypotheses(root, session)
    next_id, next_hyp, reason = get_next_hypothesis(hypotheses)

    if next_id is None:
        if args.json:
            print(json.dumps({
                "status": reason,
                "action": "EXPAND_HYPOTHESES"
            }))
        else:
            print(f"{'='*60}")
            print("NO ACTIVE HYPOTHESES")
            print(f"{'='*60}")
            if reason == "NO_ACTIVE_HYPOTHESES_UNLIKELY_REMAIN":
                print("\nAll hypotheses have been soft-eliminated (unlikely).")
                print("Consider:")
                print("  1. Resurrecting unlikely hypotheses with new evidence")
                print("  2. Adding new hypotheses")
            else:
                print("\nNo hypotheses remaining.")
                print("Run eliminate_init.py --force to start fresh with new hypotheses.")
        sys.exit(0)

    # Calculate some stats
    active_count = sum(1 for h in hypotheses.values() if h["status"] == "active")
    eliminated_count = sum(1 for h in hypotheses.values() if h["status"] == "eliminated")
    unlikely_count = sum(1 for h in hypotheses.values() if h["status"] == "unlikely")

    if args.json:
        print(json.dumps({
            "status": "CONTINUE",
            "next_hypothesis": {
                "id": next_id,
                "description": next_hyp["description"],
                "category": next_hyp["category"],
                "confidence": next_hyp["confidence"],
                "test_count": len(next_hyp.get("evidence_ids", []))
            },
            "selection_reason": reason,
            "suggested_test": suggest_test(next_hyp),
            "session_stats": {
                "iteration": session["current_iteration"],
                "active": active_count,
                "unlikely": unlikely_count,
                "eliminated": eliminated_count
            }
        }, indent=2))
    else:
        print(f"{'='*60}")
        print("NEXT ACTION")
        print(f"{'='*60}")
        print(f"\nIteration: {session['current_iteration'] + 1} / {session['max_iterations']}")
        print(f"Active: {active_count} | Unlikely: {unlikely_count} | Eliminated: {eliminated_count}")
        print(f"\n{'='*60}")
        print(f"TEST HYPOTHESIS: {next_id}")
        print(f"{'='*60}")
        print(f"\nDescription: {next_hyp['description']}")
        print(f"Category: {next_hyp['category']}")
        print(f"Confidence: {next_hyp['confidence']:.2f}")
        print(f"Times tested: {len(next_hyp.get('evidence_ids', []))}")
        print(f"Selection reason: {reason}")
        print(f"\n--- Suggested Approach ---")
        print(suggest_test(next_hyp))
        print(f"\n--- After Testing ---")
        print(f"Run: python eliminate_checkpoint.py --test '...' --evidence '...' --updates '...'")
        print(f"\nREMEMBER: Update ALL hypothesis confidences, not just {next_id}!")

        # Show current hypothesis list for reference
        print(f"\n{'='*60}")
        print("Current Hypothesis Status")
        print(f"{'='*60}")
        sorted_hyps = sorted(hypotheses.items(), key=lambda x: x[1]["confidence"], reverse=True)
        print(f"{'ID':<10} {'Confidence':>10} {'Status':<12} Description")
        print("-" * 70)
        for hid, h in sorted_hyps:
            marker = " <-- TEST THIS" if hid == next_id else ""
            print(f"{hid:<10} {h['confidence']:>10.2f} {h['status']:<12} {h['description'][:35]}...{marker}")

if __name__ == "__main__":
    main()
