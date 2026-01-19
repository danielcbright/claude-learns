#!/usr/bin/env python3
"""
Generate manifest.yaml for claude-learns template updates.

This script scans the template directory and generates a manifest.yaml file
with SHA256 checksums for all updateable files. Run this after making changes
to template files to update the manifest.

Usage:
    python generate-manifest.py [--version VERSION]

Example:
    python generate-manifest.py --version 1.2.0
"""

import argparse
import hashlib
import os
import sys
from datetime import datetime
from pathlib import Path


def get_sha256(filepath: Path) -> str:
    """Calculate SHA256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def find_template_root() -> Path:
    """Find the template directory root."""
    # Script is at template/.claude/scripts/generate-manifest.py
    script_dir = Path(__file__).resolve().parent
    template_root = script_dir.parent.parent  # Go up to template/

    if not (template_root / ".claude").exists():
        raise RuntimeError(f"Could not find template root. Expected at {template_root}")

    return template_root


def collect_files(template_root: Path) -> dict:
    """Collect all updateable files organized by category."""
    files = {
        "always_update": [],
        "updateable": [],
        "merge_only": [],
    }

    # Always update - the update command itself
    always_update_files = [
        ".claude/commands/claude-learns.update.md",
    ]

    # Updateable - commands (excluding the update command)
    command_dir = template_root / ".claude" / "commands"
    if command_dir.exists():
        for f in sorted(command_dir.glob("*.md")):
            rel_path = f".claude/commands/{f.name}"
            if rel_path in always_update_files:
                continue
            files["updateable"].append(rel_path)

    # Updateable - elimination scripts
    scripts_dir = template_root / ".claude" / "scripts" / "elimination"
    if scripts_dir.exists():
        for f in sorted(scripts_dir.glob("*.py")):
            files["updateable"].append(f".claude/scripts/elimination/{f.name}")

    # Updateable - skills
    skills_dir = template_root / ".claude" / "skills"
    if skills_dir.exists():
        for skill_dir in sorted(skills_dir.iterdir()):
            if skill_dir.is_dir():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    files["updateable"].append(f".claude/skills/{skill_dir.name}/SKILL.md")

    # Merge only - config files
    merge_only_files = [
        ".elimination/config.yaml",
        ".elimination/learned/heuristics.yaml",
        ".specify/config.yaml",
    ]
    for config_path in merge_only_files:
        if (template_root / config_path).exists():
            files["merge_only"].append(config_path)

    # Always update files
    for path in always_update_files:
        if (template_root / path).exists():
            files["always_update"].append(path)

    return files


def generate_manifest(template_root: Path, version: str) -> str:
    """Generate the manifest.yaml content."""
    files = collect_files(template_root)
    today = datetime.now().strftime("%Y-%m-%d")

    lines = [
        "# claude-learns Template Manifest",
        "# This file lists all updateable template files with their checksums.",
        "# Used by /claude-learns.update to sync template files to adopted projects.",
        "#",
        f"# Generated: {today}",
        "# To regenerate: python .claude/scripts/generate-manifest.py",
        "",
        f'version: "{version}"',
        f'generated: "{today}"',
        'base_url: "https://raw.githubusercontent.com/danielcbright/claude-learns/main/template"',
        "",
        "files:",
    ]

    # Always update section
    lines.extend([
        "  # ==========================================================================",
        "  # ALWAYS UPDATE",
        "  # These files are critical for the update mechanism and are always replaced.",
        "  # ==========================================================================",
        "  always_update:",
    ])
    for path in files["always_update"]:
        checksum = get_sha256(template_root / path)
        lines.append(f'    - path: "{path}"')
        lines.append(f'      checksum: "sha256:{checksum}"')

    # Updateable section
    lines.extend([
        "",
        "  # ==========================================================================",
        "  # UPDATEABLE",
        "  # These files can be updated with conflict detection.",
        "  # If user has modified them, they'll be asked to choose: keep local or update.",
        "  # ==========================================================================",
        "  updateable:",
    ])

    # Group updateable files by type
    commands_core = []
    commands_learn = []
    commands_elim = []
    commands_spec = []
    scripts = []
    skills = []

    for path in files["updateable"]:
        if path.startswith(".claude/commands/"):
            name = Path(path).stem
            if name.startswith("claude-learns.eliminate") or name.startswith("claude-learns.hypothesis") or \
               name.startswith("claude-learns.evidence") or name.startswith("claude-learns.bisect"):
                commands_elim.append(path)
            elif name.startswith("claude-learns.spec"):
                commands_spec.append(path)
            elif name.startswith("claude-learns."):
                commands_learn.append(path)
            else:
                commands_core.append(path)
        elif path.startswith(".claude/scripts/"):
            scripts.append(path)
        elif path.startswith(".claude/skills/"):
            skills.append(path)

    # Commands - Core
    if commands_core:
        lines.extend([
            "    # -------------------------------------------------------------------------",
            "    # Commands - Core",
            "    # -------------------------------------------------------------------------",
        ])
        for path in sorted(commands_core):
            checksum = get_sha256(template_root / path)
            lines.append(f'    - path: "{path}"')
            lines.append(f'      checksum: "sha256:{checksum}"')

    # Commands - Learning & Audit
    if commands_learn:
        lines.extend([
            "",
            "    # -------------------------------------------------------------------------",
            "    # Commands - Learning & Audit",
            "    # -------------------------------------------------------------------------",
        ])
        for path in sorted(commands_learn):
            checksum = get_sha256(template_root / path)
            lines.append(f'    - path: "{path}"')
            lines.append(f'      checksum: "sha256:{checksum}"')

    # Commands - Elimination Debugging
    if commands_elim:
        lines.extend([
            "",
            "    # -------------------------------------------------------------------------",
            "    # Commands - Elimination Debugging",
            "    # -------------------------------------------------------------------------",
        ])
        for path in sorted(commands_elim):
            checksum = get_sha256(template_root / path)
            lines.append(f'    - path: "{path}"')
            lines.append(f'      checksum: "sha256:{checksum}"')

    # Commands - Specification System
    if commands_spec:
        lines.extend([
            "",
            "    # -------------------------------------------------------------------------",
            "    # Commands - Specification System",
            "    # -------------------------------------------------------------------------",
        ])
        for path in sorted(commands_spec):
            checksum = get_sha256(template_root / path)
            lines.append(f'    - path: "{path}"')
            lines.append(f'      checksum: "sha256:{checksum}"')

    # Scripts - Elimination
    if scripts:
        lines.extend([
            "",
            "    # -------------------------------------------------------------------------",
            "    # Scripts - Elimination",
            "    # -------------------------------------------------------------------------",
        ])
        for path in sorted(scripts):
            checksum = get_sha256(template_root / path)
            lines.append(f'    - path: "{path}"')
            lines.append(f'      checksum: "sha256:{checksum}"')

    # Skills
    if skills:
        lines.extend([
            "",
            "    # -------------------------------------------------------------------------",
            "    # Skills",
            "    # -------------------------------------------------------------------------",
        ])
        for path in sorted(skills):
            checksum = get_sha256(template_root / path)
            lines.append(f'    - path: "{path}"')
            lines.append(f'      checksum: "sha256:{checksum}"')

    # Merge only section
    lines.extend([
        "",
        "  # ==========================================================================",
        "  # MERGE ONLY",
        "  # Config files where new keys are added but existing values are preserved.",
        "  # ==========================================================================",
        "  merge_only:",
    ])
    for path in files["merge_only"]:
        checksum = get_sha256(template_root / path)
        lines.append(f'    - path: "{path}"')
        lines.append(f'      checksum: "sha256:{checksum}"')

    # Protected section
    lines.extend([
        "",
        "  # ==========================================================================",
        "  # PROTECTED",
        "  # These paths are NEVER modified by /update. Listed for documentation only.",
        "  # ==========================================================================",
        "  protected:",
        '    - ".serena/memories/*"',
        '    - ".specify/specs/*"',
        '    - ".specify/memory/constitution.md"',
        '    - ".specify/memory/corrections.md"',
        '    - ".elimination/active/*"',
        '    - ".elimination/archive/*"',
    ])

    # Original checksums section
    lines.extend([
        "",
        "# ==========================================================================",
        "# ORIGINAL CHECKSUMS",
        "# Used for conflict detection: if local differs from both original AND latest,",
        "# user has modified the file and needs to choose what to do.",
        "#",
        "# Initially, original_checksums = current checksums (fresh install).",
        "# After an update, original_checksums are updated to the NEW checksums,",
        "# so future updates can detect user modifications.",
        "# ==========================================================================",
        "original_checksums:",
    ])

    # Collect all file paths for original checksums
    all_files = files["always_update"] + files["updateable"] + files["merge_only"]
    for path in sorted(all_files):
        checksum = get_sha256(template_root / path)
        lines.append(f'  "{path}": "sha256:{checksum}"')

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate manifest.yaml for claude-learns template")
    parser.add_argument("--version", default="1.1.0", help="Version string for the manifest")
    parser.add_argument("--output", help="Output file path (default: template/manifest.yaml)")
    parser.add_argument("--dry-run", action="store_true", help="Print to stdout instead of writing file")
    args = parser.parse_args()

    try:
        template_root = find_template_root()
        manifest_content = generate_manifest(template_root, args.version)

        if args.dry_run:
            print(manifest_content)
        else:
            output_path = Path(args.output) if args.output else template_root / "manifest.yaml"
            output_path.write_text(manifest_content)
            print(f"Generated manifest at: {output_path}")

            # Count files
            files = collect_files(template_root)
            total = sum(len(v) for v in files.values())
            print(f"  - always_update: {len(files['always_update'])} files")
            print(f"  - updateable: {len(files['updateable'])} files")
            print(f"  - merge_only: {len(files['merge_only'])} files")
            print(f"  - Total: {total} files")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
