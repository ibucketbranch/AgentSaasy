# Cursor Rules for AgentSaaSy_EAM

Modern `.cursor/rules/` structure for AI-assisted development of the enterprise asset management AI agent.

## Overview

This directory contains 8 specialized rule files that provide context and standards for AI code generation:

| File | Purpose | Auto-Apply | Lines |
|------|---------|-----------|-------|
| `project-context.mdc` | Project identity, architecture, current state | ✅ Yes | ~100 |
| `domain-asset-management.mdc` | Asset management domain knowledge | 🔧 On *.py, *.md | ~200 |
| `langchain-agent-dev.mdc` | LangChain agent development patterns | 🔧 On agent.py, test_*.py | ~300 |
| `python-style.mdc` | Python 3.10+ coding standards | 🔧 On *.py | ~300 |
| `testing-qa.mdc` | Pytest testing strategies | 🔧 On test_*.py | ~350 |
| `documentation.mdc` | Markdown documentation standards | 🔧 On *.md | ~300 |
| `git-workflow.mdc` | Git commits, branching, version control | 🔧 On .git, .gitignore | ~400 |
| `data-science.mdc` | Pandas, NumPy, scikit-learn best practices | 🔧 On *.py | ~350 |

**Total**: ~2,300 lines of specialized guidance

## Rule Categories

### 1. **Always-On Context** (`project-context.mdc`)
- Loaded on every interaction
- Project identity (AgentSaaSy_EAM)
- 3-layer architecture
- 5 tools (query_assets, analyze_asset_health, etc.)
- Current state and metrics
- Critical rules (NEVER delete without confirmation)

### 2. **Domain Knowledge** (`domain-asset-management.mdc`)
- Asset management terminology
- Health score calculations
- Risk assessment formulas
- Data model schema
- AgentSaaSy AM platform context
- Business value language

### 3. **Technical Standards**
- **`langchain-agent-dev.mdc`**: ReAct pattern, tool definitions, prompt engineering
- **`python-style.mdc`**: Type hints, naming, error handling, pathlib
- **`testing-qa.mdc`**: Unit tests, integration tests, pytest fixtures
- **`data-science.mdc`**: pandas operations, numpy, scikit-learn patterns

### 4. **Process & Workflow**
- **`documentation.mdc`**: 4-file structure, markdown style, audience-first writing
- **`git-workflow.mdc`**: Commit messages, branching, merge strategy

## How Rules Are Applied

### Auto-Apply (project-context.mdc)
Loaded in every Cursor session automatically.

### File Pattern Matching (globs)
Rules auto-attach when you open matching files:
```yaml
globs: ["*.py", "**/*.py"]      # Python files
globs: ["*.md", "**/*.md"]      # Markdown files
globs: ["test_*.py"]            # Test files
globs: ["agent.py", "**/agent*.py"]  # Agent files
```

### AI Agent Requested
Cursor's AI decides when to load specific rules based on your query.

## Usage Examples

### Editing agent.py
**Auto-loaded rules**:
- `project-context.mdc` (always on)
- `python-style.mdc` (*.py glob)
- `langchain-agent-dev.mdc` (agent.py glob)
- `data-science.mdc` (*.py glob)

**AI can request**: `domain-asset-management.mdc`, `testing-qa.mdc`

### Writing tests/test_agent.py
**Auto-loaded rules**:
- `project-context.mdc` (always on)
- `python-style.mdc` (*.py glob)
- `testing-qa.mdc` (test_*.py glob)
- `langchain-agent-dev.mdc` (test_*.py glob)

### Updating README.md
**Auto-loaded rules**:
- `project-context.mdc` (always on)
- `documentation.mdc` (*.md glob)
- `domain-asset-management.mdc` (*.md glob)

### Committing changes
**Auto-loaded rules**:
- `git-workflow.mdc` (.git, .gitignore globs)

## Key Principles Across All Rules

### 1. Context First
Always understand the system before making changes:
- Read files before editing
- Check existing patterns
- Run tests after changes

### 2. Domain Accuracy
Use asset management terminology, not sales:
- ✅ asset, health_score, maintenance, compliance
- ❌ sales, revenue, product, customer

### 3. Professional Quality
Production-ready code standards:
- Type hints on all functions
- Comprehensive error handling
- 100% test coverage
- Clear documentation

### 4. Explicit Confirmation
**NEVER delete files without per-file confirmation** from the user.

## Customization

### Adding New Rules
1. Create `your-rule.mdc` in this directory
2. Add YAML frontmatter:
   ```yaml
   ---
   name: "Your Rule Name"
   description: "When to use this rule"
   tags: ["tag1", "tag2"]
   globs: ["*.py"]  # Optional: auto-attach pattern
   alwaysApply: false  # true = always on
   ---
   ```
3. Write content in markdown

### Modifying Existing Rules
Edit the `.mdc` files directly. Changes take effect immediately in new Cursor sessions.

### Disabling Rules Temporarily
Rename file extension:
```bash
mv domain-asset-management.mdc domain-asset-management.mdc.disabled
```

## Rule Maintenance

### When to Update
- **Code changes**: Update `langchain-agent-dev.mdc`, `python-style.mdc`
- **New features**: Update `project-context.mdc`, `domain-asset-management.mdc`
- **Process changes**: Update `git-workflow.mdc`, `testing-qa.mdc`
- **Documentation changes**: Update `documentation.mdc`

### Quality Checks
- [ ] All code examples tested and working
- [ ] No outdated references
- [ ] Consistent terminology
- [ ] Clear, actionable guidance

## Migration Notes

### From Old `.cursorrules`
The original single `.cursorrules` file (59 lines) has been split into 8 specialized files (~2,300 lines total) for:
- **Better organization**: Topic-based files
- **Selective loading**: Only relevant rules apply
- **Easier maintenance**: Update one area at a time
- **Scalability**: Add new rules without bloating one file

### Backward Compatibility
The old `.cursorrules` file can coexist with this structure, but we recommend:
1. Delete old `.cursorrules` (it's now gitignored)
2. Use this modern `.cursor/rules/` structure

## Performance

### Loading Time
- **Auto-apply rules**: ~100 lines (instant)
- **File-matched rules**: ~300-400 lines each (negligible)
- **AI-requested rules**: Loaded on demand

### Token Usage
- Rules are part of system prompt
- Only relevant rules loaded per session
- Estimated 500-2000 tokens (negligible vs 200k context window)

## Resources

### Cursor Documentation
- [Cursor Rules Guide](https://docs.cursor.com/context/rules-for-ai)
- [.mdc File Format](https://docs.cursor.com/context/rules-for-ai#mdc-file-format)

### Project Documentation
- [PROJECT-DICTIONARY.md](../PROJECT-DICTIONARY.md) - Terminology reference
- [ARCHITECTURE.md](../ARCHITECTURE.md) - System design
- [README.md](../README.md) - Project overview

## Support

For questions or issues with these rules:
1. Check rule file comments for examples
2. Consult project documentation
3. Ask Cursor AI to explain a specific rule

---

**Last Updated**: 2024-01-XX  
**Maintained By**: AgentSaaSy AM Team  
**Version**: 1.0.0
