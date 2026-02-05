#!/usr/bin/env bash
# sync-to-template.sh - Sync root development files to template/
#
# Usage:
#   ./scripts/sync-to-template.sh [--force] [--dry-run]
#
# This script helps maintain the dual-location architecture by syncing
# development files from root to template/ with safety checks.

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Detect repo root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Parse arguments
FORCE=0
DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case $1 in
    --force) FORCE=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help)
      echo "Usage: $0 [--force] [--dry-run]"
      echo ""
      echo "Options:"
      echo "  --force     Override warnings and proceed with sync"
      echo "  --dry-run   Show what would be synced without doing it"
      echo "  --help      Show this help message"
      exit 0
      ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# Helper functions
error() {
  echo -e "${RED}ERROR:${NC} $1" >&2
}

warn() {
  echo -e "${YELLOW}WARNING:${NC} $1"
}

info() {
  echo -e "${GREEN}✓${NC} $1"
}

# Pre-flight checks
check_preconditions() {
  # Check we're in the right directory
  if [[ ! -d "template" ]] || [[ ! -d ".claude" ]]; then
    error "Must run from claude-learns project root"
    exit 1
  fi

  # Warn if git working directory is dirty
  if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    warn "Git working directory is dirty. Recommend committing changes first."
    if [[ $FORCE -eq 0 ]]; then
      echo "Use --force to proceed anyway"
      exit 1
    fi
  fi
}

# Violation checks
check_violations() {
  local violations=0

  # Check for dev-specific content in root files
  if grep -rq "danielcbright\|/root/claudebot" .claude/commands/ .claude/scripts/ 2>/dev/null; then
    warn "Found dev-specific paths in command/script files"
    violations=$((violations + 1))
  fi

  # Check template files still have placeholders
  if [[ -f "template/CLAUDE.md" ]]; then
    if ! grep -q "\[PROJECT_NAME\]" template/CLAUDE.md; then
      warn "template/CLAUDE.md missing [PROJECT_NAME] placeholder"
      violations=$((violations + 1))
    fi
  fi

  # Check for unexpected files in template active directories
  local unexpected_files
  unexpected_files=$(find template/.elimination/active template/.elimination/archive \
                          -type f ! -name '.gitkeep' 2>/dev/null | wc -l)
  if [[ $unexpected_files -gt 0 ]]; then
    warn "Found $unexpected_files unexpected files in template/.elimination/active or archive"
    violations=$((violations + 1))
  fi

  if [[ $violations -gt 0 ]] && [[ $FORCE -eq 0 ]]; then
    echo ""
    error "Found $violations violation(s). Use --force to proceed anyway."
    exit 1
  elif [[ $violations -gt 0 ]]; then
    warn "Proceeding with $violations violation(s) due to --force"
  fi

  return 0
}

# Sync function
sync_files() {
  local file_count=0

  # Enable nullglob so patterns that don't match expand to nothing
  shopt -s nullglob

  # Category A: Direct sync (safe)
  local patterns=(
    ".claude/commands/*.md"
    ".claude/scripts/elimination/*.py"
    ".claude/skills/*/SKILL.md"
    ".claude/aliases.yaml"
    ".claude/update-registry.yaml"
    ".elimination/config.yaml"
    ".specify/config.yaml"
  )

  for pattern in "${patterns[@]}"; do
    for file in $pattern; do
      if [[ ! -f "$file" ]]; then continue; fi

      local target="template/$file"
      local action="Sync"

      if [[ $DRY_RUN -eq 1 ]]; then
        echo "[DRY-RUN] Would sync: $file -> $target"
        file_count=$((file_count + 1))
      else
        mkdir -p "$(dirname "$target")"
        cp "$file" "$target"
        info "Synced: $file"
        file_count=$((file_count + 1))
      fi
    done
  done

  echo ""
  info "Synced $file_count files"
}

# Manifest regeneration
regenerate_manifest() {
  if [[ $DRY_RUN -eq 1 ]]; then
    echo ""
    echo "[DRY-RUN] Would regenerate manifest with version 1.2"
    return
  fi

  echo ""
  info "Regenerating manifest..."
  if python3 .claude/scripts/generate-manifest.py --version 1.2 2>&1; then
    info "Manifest updated"
  else
    error "Manifest generation failed"
    exit 1
  fi
}

# Show changes
show_changes() {
  if [[ $DRY_RUN -eq 1 ]]; then
    return
  fi

  echo ""
  echo "═══════════════════════════════════════════════════════════════════════════"
  echo "Review changes with: git diff template/"
  echo "═══════════════════════════════════════════════════════════════════════════"
}

# Main execution
main() {
  echo "═══════════════════════════════════════════════════════════════════════════"
  echo "Claude-Learns Template Sync"
  echo "═══════════════════════════════════════════════════════════════════════════"
  echo ""

  check_preconditions

  if [[ $FORCE -eq 0 ]]; then
    check_violations
  fi

  sync_files
  regenerate_manifest
  show_changes

  echo ""
  info "Sync complete!"
}

main "$@"
