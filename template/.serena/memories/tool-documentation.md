# Tool Documentation References

> Official documentation sources for all integrated tools. Always fetch latest docs before implementation.

---

## Purpose

This memory provides:
- Links to official documentation for all tools
- Instructions for fetching up-to-date docs via Context7
- Version tracking for documentation references

## When to Read

- Before implementing features that use external tools
- When unsure about API behavior or best practices
- When documentation in code comments seems outdated

## When to Update

- When adding new tool integrations
- When tool versions change significantly
- When better documentation sources are discovered

---

## Core Tool Documentation

### Claude Code

| Resource | Location |
|----------|----------|
| Official Docs | https://docs.anthropic.com/claude-code |
| GitHub | https://github.com/anthropics/claude-code |
| Context7 Query | `mcp__context7__resolve-library-id("anthropic claude-code")` |

### Serena MCP

| Resource | Location |
|----------|----------|
| GitHub | https://github.com/oraios/serena |
| Context7 Query | `mcp__context7__resolve-library-id("serena mcp")` |

**Key Features**:
- Symbol-level code navigation
- Semantic code editing
- Memory management via `.serena/memories/`

### Context7 MCP

| Resource | Location |
|----------|----------|
| Self-documenting | Use `resolve-library-id` for any library |
| Query Pattern | `mcp__context7__resolve-library-id("[library name]")` |

**Usage Pattern**:
```
1. Resolve library ID: resolve-library-id("react")
2. Query docs: query-docs("/vercel/react", "how to use hooks")
```

### Spec-Kit

| Resource | Location |
|----------|----------|
| GitHub | https://github.com/github/spec-kit |
| Context7 Query | `mcp__context7__resolve-library-id("github spec-kit")` |

**Key Concepts**:
- Specification-driven development
- Constitution for invariants
- Deviation tracking

---

## MCP Server Documentation

### Available MCPs

| MCP | Purpose | Context7 Query |
|-----|---------|----------------|
| Serena | Code navigation | `resolve-library-id("serena mcp")` |
| Context7 | Library docs | Self-documenting |
| Sequential Thinking | Complex reasoning | N/A (built-in) |
| Playwright | Browser automation | `resolve-library-id("playwright")` |

### MCP Configuration

```bash
# Add Serena MCP
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context claude-code --project $(pwd)

# Check MCP status
/mcp
```

---

## Framework Documentation

### [FRAMEWORK_1]

| Resource | Location |
|----------|----------|
| Official Docs | [URL] |
| Context7 Query | `resolve-library-id("[framework]")` |
| Version Used | [version] |

---

## Fetching Latest Documentation

### Before Implementation

Always fetch current docs for unfamiliar APIs:

```
# Step 1: Resolve library ID
mcp__context7__resolve-library-id("library-name")

# Step 2: Query specific topic
mcp__context7__query-docs("/org/library", "specific topic or question")
```

### Example Queries

```
# React hooks
resolve-library-id("react") → query-docs("/vercel/react", "useEffect cleanup")

# Express middleware
resolve-library-id("express") → query-docs("/expressjs/express", "error handling middleware")

# Spec-kit usage
resolve-library-id("github spec-kit") → query-docs("/github/spec-kit", "creating specifications")
```

---

## Version Tracking

Track versions of key dependencies to ensure doc compatibility:

| Tool/Library | Version | Last Verified | Doc Source |
|--------------|---------|---------------|------------|
| Claude Code | current | 2026-01-17 | Anthropic docs |
| Serena MCP | current | 2026-01-17 | GitHub |
| [Framework] | [version] | [date] | [source] |

---

## Documentation Gaps

Known areas where documentation is limited:

| Area | Issue | Workaround |
|------|-------|------------|
| [Area] | [What's missing] | [How to work around] |

---

## Contributing to This Memory

When you discover useful documentation:
1. Add the resource to the appropriate section
2. Include Context7 query if available
3. Note any version-specific caveats
4. Update the "Last Verified" date

---

*Last Updated: 2026-01-17*
*Documentation Sources: 4 primary tools*
