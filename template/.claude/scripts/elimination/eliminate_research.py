#!/usr/bin/env python3
"""
eliminate_research.py - Research hypotheses using online sources

Searches for supporting evidence from:
- GitHub Issues
- Stack Overflow
- General web search
- Official documentation

Usage:
    python eliminate_research.py --hypothesis H1
    python eliminate_research.py --all
    python eliminate_research.py --symptom "API 500 errors on login"

The script generates search queries and provides URLs/summaries for Claude
to investigate using WebFetch or WebSearch tools.
"""

import argparse
import sys
import yaml
import json
import urllib.parse
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

def detect_tech_stack(root: Path) -> dict:
    """Detect technology stack from project files."""
    tech = {
        "languages": [],
        "frameworks": [],
        "databases": [],
        "tools": []
    }

    # Check for common project files
    indicators = {
        "package.json": {"languages": ["JavaScript", "TypeScript"], "frameworks": ["Node.js"]},
        "requirements.txt": {"languages": ["Python"]},
        "pyproject.toml": {"languages": ["Python"]},
        "Cargo.toml": {"languages": ["Rust"]},
        "go.mod": {"languages": ["Go"]},
        "pom.xml": {"languages": ["Java"], "frameworks": ["Maven"]},
        "build.gradle": {"languages": ["Java", "Kotlin"], "frameworks": ["Gradle"]},
        "Gemfile": {"languages": ["Ruby"]},
        "composer.json": {"languages": ["PHP"]},
        "docker-compose.yml": {"tools": ["Docker"]},
        "Dockerfile": {"tools": ["Docker"]},
        ".env": {"tools": ["dotenv"]},
    }

    for filename, techs in indicators.items():
        if (root / filename).exists():
            for key, values in techs.items():
                tech[key].extend(values)

    # Check package.json for specific frameworks
    pkg_json = root / "package.json"
    if pkg_json.exists():
        try:
            with open(pkg_json, 'r') as f:
                pkg = json.load(f)
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

            framework_indicators = {
                "react": "React",
                "next": "Next.js",
                "vue": "Vue.js",
                "angular": "Angular",
                "express": "Express.js",
                "fastify": "Fastify",
                "nestjs": "NestJS",
                "prisma": "Prisma",
                "mongoose": "MongoDB",
                "pg": "PostgreSQL",
                "mysql": "MySQL",
                "redis": "Redis",
            }

            for dep, framework in framework_indicators.items():
                if any(dep in d.lower() for d in deps.keys()):
                    if framework in ["MongoDB", "PostgreSQL", "MySQL", "Redis"]:
                        tech["databases"].append(framework)
                    else:
                        tech["frameworks"].append(framework)
        except:
            pass

    # Deduplicate
    for key in tech:
        tech[key] = list(set(tech[key]))

    return tech

def generate_search_queries(hypothesis: dict, symptom: str, tech_stack: dict) -> list:
    """Generate search queries for a hypothesis."""
    queries = []

    desc = hypothesis.get("description", "")
    category = hypothesis.get("category", "Code")

    # Build tech context string
    tech_terms = []
    tech_terms.extend(tech_stack.get("languages", []))
    tech_terms.extend(tech_stack.get("frameworks", []))
    tech_context = " ".join(tech_terms[:3])  # Limit to avoid too long queries

    # Category-specific query patterns
    category_patterns = {
        "Code": [
            f"{desc} {tech_context}",
            f"{symptom} bug {tech_context}",
            f"{desc} fix solution",
        ],
        "Config": [
            f"{desc} configuration {tech_context}",
            f"{symptom} config environment variable",
            f"{desc} settings",
        ],
        "Dependencies": [
            f"{desc} version conflict {tech_context}",
            f"{symptom} dependency issue",
            f"{desc} breaking change",
        ],
        "Data": [
            f"{desc} data corruption",
            f"{symptom} invalid data edge case",
            f"{desc} validation",
        ],
        "Infrastructure": [
            f"{desc} server resource",
            f"{symptom} timeout memory CPU",
            f"{desc} infrastructure",
        ],
        "Concurrency": [
            f"{desc} race condition {tech_context}",
            f"{symptom} deadlock thread",
            f"{desc} concurrent async",
        ],
    }

    base_queries = category_patterns.get(category, [f"{desc} {tech_context}"])

    for q in base_queries:
        queries.append({
            "query": q.strip(),
            "type": "general"
        })

    return queries

def generate_github_search(hypothesis: dict, symptom: str, tech_stack: dict) -> list:
    """Generate GitHub-specific search queries."""
    searches = []

    desc = hypothesis.get("description", "")

    # Extract potential error messages or keywords
    keywords = []
    for word in desc.split():
        if len(word) > 4 and word[0].isupper():
            keywords.append(word)

    # GitHub Issues search
    base_query = f"{desc}"
    if tech_stack.get("frameworks"):
        base_query += f" {tech_stack['frameworks'][0]}"

    searches.append({
        "url": f"https://github.com/search?q={urllib.parse.quote(base_query)}&type=issues",
        "description": f"GitHub Issues: {base_query[:50]}...",
        "type": "github_issues"
    })

    # If we know specific repos/orgs from package.json, search there
    # This is a placeholder - in practice you'd extract repo info

    return searches

def generate_stackoverflow_search(hypothesis: dict, symptom: str, tech_stack: dict) -> list:
    """Generate Stack Overflow search queries."""
    searches = []

    desc = hypothesis.get("description", "")

    # Build tagged search
    tags = []
    for lang in tech_stack.get("languages", []):
        tags.append(lang.lower())
    for fw in tech_stack.get("frameworks", []):
        tags.append(fw.lower().replace(".", "").replace(" ", "-"))

    tag_str = "+".join(tags[:3]) if tags else ""

    query = f"{desc}"
    if tag_str:
        url = f"https://stackoverflow.com/search?q={urllib.parse.quote(query)}+[{tag_str}]"
    else:
        url = f"https://stackoverflow.com/search?q={urllib.parse.quote(query)}"

    searches.append({
        "url": url,
        "description": f"Stack Overflow: {query[:50]}...",
        "type": "stackoverflow"
    })

    # Also search with symptom
    symptom_query = f"{symptom}"
    if tag_str:
        url2 = f"https://stackoverflow.com/search?q={urllib.parse.quote(symptom_query)}+[{tag_str}]"
    else:
        url2 = f"https://stackoverflow.com/search?q={urllib.parse.quote(symptom_query)}"

    searches.append({
        "url": url2,
        "description": f"Stack Overflow (symptom): {symptom_query[:50]}...",
        "type": "stackoverflow"
    })

    return searches

def generate_research_plan(hypothesis: dict, symptom: str, tech_stack: dict) -> dict:
    """Generate a complete research plan for a hypothesis."""
    plan = {
        "hypothesis_id": hypothesis.get("id", "unknown"),
        "hypothesis_description": hypothesis.get("description", ""),
        "generated_at": datetime.now().isoformat(),
        "tech_context": tech_stack,
        "search_queries": generate_search_queries(hypothesis, symptom, tech_stack),
        "github_searches": generate_github_search(hypothesis, symptom, tech_stack),
        "stackoverflow_searches": generate_stackoverflow_search(hypothesis, symptom, tech_stack),
        "suggested_actions": []
    }

    # Add suggested actions for Claude
    plan["suggested_actions"] = [
        {
            "action": "web_search",
            "query": plan["search_queries"][0]["query"] if plan["search_queries"] else symptom,
            "tool": "WebSearch",
            "priority": "high"
        },
        {
            "action": "fetch_github_issues",
            "url": plan["github_searches"][0]["url"] if plan["github_searches"] else None,
            "tool": "WebFetch",
            "priority": "high"
        },
        {
            "action": "fetch_stackoverflow",
            "url": plan["stackoverflow_searches"][0]["url"] if plan["stackoverflow_searches"] else None,
            "tool": "WebFetch",
            "priority": "medium"
        }
    ]

    return plan

def record_research_findings(root: Path, hyp_id: str, findings: dict):
    """Record research findings in the hypothesis file."""
    hyp = load_hypothesis(root, hyp_id)
    if not hyp:
        return False

    # Add research section
    if "research" not in hyp:
        hyp["research"] = []

    hyp["research"].append({
        "timestamp": datetime.now().isoformat(),
        "findings": findings
    })

    # If strong supporting evidence found, boost confidence
    if findings.get("confidence_boost"):
        old_conf = hyp["confidence"]
        boost = min(findings["confidence_boost"], 0.20)  # Cap at 0.20 boost
        new_conf = min(old_conf + boost, 0.95)  # Cap at 0.95

        hyp["confidence"] = new_conf
        hyp["confidence_history"].append({
            "timestamp": datetime.now().isoformat(),
            "confidence": new_conf,
            "reason": f"Research evidence: {findings.get('summary', 'Online sources support this hypothesis')[:50]}"
        })

    save_hypothesis(root, hyp_id, hyp)
    return True

def main():
    parser = argparse.ArgumentParser(description="Research hypotheses using online sources")
    parser.add_argument("--hypothesis", "-h", dest="hyp_id", help="Specific hypothesis to research (H1, H2, or hyp-001)")
    parser.add_argument("--all", "-a", action="store_true", help="Research all active hypotheses")
    parser.add_argument("--symptom", "-s", help="Override symptom for search queries")
    parser.add_argument("--record", "-r", help="Record findings as JSON string")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--boost", type=float, help="Confidence boost if recording findings (0.0-0.20)")

    args = parser.parse_args()

    root = find_project_root()
    if not root:
        print("ERROR: No .elimination directory found. Run eliminate_init.py first.")
        sys.exit(1)

    session = load_session(root)
    if not session:
        print("ERROR: No active session found. Run eliminate_init.py first.")
        sys.exit(1)

    symptom = args.symptom or session.get("symptom", "")
    tech_stack = detect_tech_stack(root)

    # If recording findings
    if args.record:
        if not args.hyp_id:
            print("ERROR: --hypothesis required when recording findings")
            sys.exit(1)

        # Normalize hypothesis ID
        ref = args.hyp_id.upper()
        if ref.startswith("H") and ref[1:].isdigit():
            hyp_id = f"hyp-{int(ref[1:]):03d}"
        else:
            hyp_id = args.hyp_id.lower()

        findings = json.loads(args.record)
        if args.boost:
            findings["confidence_boost"] = args.boost

        if record_research_findings(root, hyp_id, findings):
            print(f"Findings recorded for {hyp_id}")
            if args.boost:
                hyp = load_hypothesis(root, hyp_id)
                print(f"New confidence: {hyp['confidence']:.2f}")
        else:
            print(f"ERROR: Could not record findings for {hyp_id}")
        sys.exit(0)

    # Load hypotheses to research
    hypotheses = load_all_hypotheses(root, session)

    if args.hyp_id:
        # Single hypothesis
        ref = args.hyp_id.upper()
        if ref.startswith("H") and ref[1:].isdigit():
            hyp_id = f"hyp-{int(ref[1:]):03d}"
        else:
            hyp_id = args.hyp_id.lower()

        if hyp_id not in hypotheses:
            print(f"ERROR: Hypothesis {hyp_id} not found")
            sys.exit(1)

        target_hyps = {hyp_id: hypotheses[hyp_id]}
    elif args.all:
        # All active hypotheses
        target_hyps = {hid: h for hid, h in hypotheses.items() if h["status"] == "active"}
    else:
        # Default: highest confidence active hypothesis
        active = [(hid, h) for hid, h in hypotheses.items() if h["status"] == "active"]
        if not active:
            print("No active hypotheses to research")
            sys.exit(0)
        active.sort(key=lambda x: x[1]["confidence"], reverse=True)
        target_hyps = {active[0][0]: active[0][1]}

    # Generate research plans
    all_plans = {}
    for hyp_id, hyp in target_hyps.items():
        plan = generate_research_plan(hyp, symptom, tech_stack)
        all_plans[hyp_id] = plan

    if args.json:
        print(json.dumps(all_plans, indent=2))
        return

    # Pretty print research plan
    print(f"\n{'='*70}")
    print("RESEARCH PLAN")
    print(f"{'='*70}")
    print(f"\nSymptom: {symptom}")
    print(f"Tech Stack: {', '.join(tech_stack.get('languages', []) + tech_stack.get('frameworks', []))}")

    for hyp_id, plan in all_plans.items():
        print(f"\n{'='*70}")
        print(f"HYPOTHESIS: {hyp_id}")
        print(f"{'='*70}")
        print(f"Description: {plan['hypothesis_description']}")

        print(f"\n--- Search Queries (use with WebSearch) ---")
        for i, q in enumerate(plan["search_queries"], 1):
            print(f"{i}. {q['query']}")

        print(f"\n--- GitHub Issues (use with WebFetch) ---")
        for gh in plan["github_searches"]:
            print(f"URL: {gh['url']}")

        print(f"\n--- Stack Overflow (use with WebFetch) ---")
        for so in plan["stackoverflow_searches"]:
            print(f"URL: {so['url']}")

        print(f"\n--- Suggested Actions for Claude ---")
        for action in plan["suggested_actions"]:
            if action.get("url") or action.get("query"):
                print(f"  [{action['priority'].upper()}] {action['action']}")
                if action.get("query"):
                    print(f"    Tool: {action['tool']}")
                    print(f"    Query: {action['query']}")
                if action.get("url"):
                    print(f"    Tool: {action['tool']}")
                    print(f"    URL: {action['url']}")

    print(f"\n{'='*70}")
    print("RECORDING FINDINGS")
    print(f"{'='*70}")
    print("""
After researching, record findings with:

  python eliminate_research.py --hypothesis H1 --record '{
    "source": "GitHub Issue #1234",
    "url": "https://github.com/...",
    "summary": "Similar issue reported, caused by race condition",
    "relevance": "high"
  }' --boost 0.15

The --boost flag increases hypothesis confidence (max 0.20).
Use higher boosts for:
  - Exact error message matches
  - Same tech stack and version
  - Confirmed fixes that match hypothesis
""")

if __name__ == "__main__":
    main()
