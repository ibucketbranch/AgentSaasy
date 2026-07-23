"""
Prompt Library — Centralized catalog and manager for all project prompts.

Follows software engineering best practices for prompt management:
  1. Single registry (YAML) as source of truth for all prompts
  2. Versioned prompt files with metadata (author, date, model, tokens)
  3. Template variable substitution via {{variable}} syntax
  4. Category-based organization (system, demo, act, query)
  5. Programmatic access for agent code and demo scripts

Usage:
    from prompt_library import PromptLibrary

    lib = PromptLibrary()
    lib.list_prompts()                              # Show all registered prompts
    lib.list_prompts(category="demo")               # Filter by category
    prompt = lib.get("demo-master-showcase")        # Get raw prompt content
    rendered = lib.render("act1-iot-anomaly",       # Render with variables
                          asset_id="PS-007",
                          sensor_type="vibration")
    lib.info("act3-budget-scenario")                # Print metadata
"""

import re
from datetime import date
from pathlib import Path
from typing import Any

import yaml

# Constants
PROMPTS_DIR = Path(__file__).parent / "prompts"
REGISTRY_PATH = PROMPTS_DIR / "registry.yaml"


class PromptLibrary:
    """Centralized prompt catalog with loading, rendering, and metadata access.

    Attributes:
        registry: Parsed YAML registry with all prompt metadata.
        prompts_dir: Path to the prompts/ directory.
    """

    def __init__(self, prompts_dir: Path | None = None) -> None:
        self.prompts_dir = prompts_dir or PROMPTS_DIR
        self.registry = self._load_registry()

    # ── Core API ──────────────────────────────────────────────

    def list_prompts(self, category: str | None = None) -> list[dict[str, Any]]:
        """List all registered prompts, optionally filtered by category.

        Args:
            category: Filter by category slug (system, demo, act, query).
                      None returns all prompts.

        Returns:
            List of prompt metadata dicts.
        """
        prompts = self.registry.get("prompts", [])
        if category:
            prompts = [p for p in prompts if p.get("category") == category]
        return prompts

    def get(self, prompt_id: str) -> str:
        """Get raw prompt content by ID (no variable substitution).

        Args:
            prompt_id: Unique prompt slug from registry (e.g. 'act1-iot-anomaly').

        Returns:
            Full markdown content of the prompt file.

        Raises:
            KeyError: If prompt_id is not found in registry.
            FileNotFoundError: If the prompt file is missing on disk.
        """
        entry = self._find_entry(prompt_id)
        file_path = self.prompts_dir / entry["file"]
        if not file_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {file_path}")
        return file_path.read_text(encoding="utf-8")

    def render(self, prompt_id: str, **variables: str) -> str:
        """Load a prompt and substitute {{variable}} placeholders.

        Args:
            prompt_id: Unique prompt slug from registry.
            **variables: Key-value pairs to substitute into the template.
                         Keys should match variable names WITHOUT braces.

        Returns:
            Rendered prompt string with variables replaced.

        Example:
            lib.render("act1-iot-anomaly", asset_id="PS-007", sensor_type="vibration")
        """
        content = self.get(prompt_id)

        # Auto-fill common variables
        variables.setdefault("demo_date", date.today().strftime("%B %d, %Y"))

        # Replace {{variable_name}} patterns
        for key, value in variables.items():
            pattern = r"\{\{\s*" + re.escape(key) + r"\s*\}\}"
            content = re.sub(pattern, str(value), content)

        return content

    def info(self, prompt_id: str) -> dict[str, Any]:
        """Get metadata for a specific prompt.

        Args:
            prompt_id: Unique prompt slug from registry.

        Returns:
            Dict with all registry metadata for the prompt.
        """
        return self._find_entry(prompt_id)

    def get_categories(self) -> dict[str, str]:
        """Return all defined categories with descriptions.

        Returns:
            Dict mapping category slug to description string.
        """
        return self.registry.get("categories", {})

    def get_system_prompt(self) -> str:
        """Convenience method to load the main system prompt for the agent.

        Returns:
            Rendered system prompt string.
        """
        return self.render("system-asset-agent")

    def get_act_prompts(self) -> list[dict[str, Any]]:
        """Return metadata for all act prompts in demo order.

        Returns:
            List of act prompt metadata dicts, sorted by ID.
        """
        acts = self.list_prompts(category="act")
        return sorted(acts, key=lambda p: p["id"])

    def get_demo_flow(self, **variables: str) -> list[dict[str, str]]:
        """Build the full 5-act demo flow with rendered prompts.

        Args:
            **variables: Variables to substitute into all act prompts.

        Returns:
            List of dicts with keys: id, name, rendered_prompt
        """
        acts = self.get_act_prompts()
        flow = []
        for act in acts:
            rendered = self.render(act["id"], **variables)
            flow.append({
                "id": act["id"],
                "name": act["name"],
                "rendered_prompt": rendered,
            })
        return flow

    # ── Display Helpers ───────────────────────────────────────

    def print_catalog(self, category: str | None = None) -> None:
        """Pretty-print the prompt catalog to stdout.

        Args:
            category: Optional category filter.
        """
        prompts = self.list_prompts(category)
        if not prompts:
            print("No prompts found.")
            return

        print()
        print("=" * 72)
        title = f"PROMPT LIBRARY — {category.upper()}" if category else "PROMPT LIBRARY — ALL PROMPTS"
        print(f"  {title}")
        print("=" * 72)

        current_cat = None
        for p in prompts:
            cat = p.get("category", "uncategorized")
            if cat != current_cat:
                current_cat = cat
                print(f"\n  [{cat.upper()}]")
                print(f"  {'─' * 66}")

            print(f"    {p['id']:<30} v{p['version']:<8} ~{p.get('est_tokens', '?')} tokens")
            print(f"      {p['name']}")

        print()
        print(f"  Total: {len(prompts)} prompt(s)")
        print("=" * 72)
        print()

    def print_info(self, prompt_id: str) -> None:
        """Pretty-print detailed metadata for a single prompt."""
        entry = self._find_entry(prompt_id)
        print()
        print(f"  Prompt: {entry['name']}")
        print(f"  ID:     {entry['id']}")
        print(f"  File:   {entry['file']}")
        print(f"  Version:{entry['version']}")
        print(f"  Category:{entry['category']}")
        print(f"  Model:  {entry.get('model', 'N/A')}")
        print(f"  Tokens: ~{entry.get('est_tokens', '?')}")
        print(f"  Author: {entry.get('author', 'Unknown')}")
        print(f"  Created:{entry.get('created', 'Unknown')}")
        if entry.get("variables"):
            print(f"  Vars:   {', '.join(entry['variables'])}")
        print(f"  Desc:   {entry.get('description', 'N/A')}")
        print()

    # ── Internal ──────────────────────────────────────────────

    def _load_registry(self) -> dict[str, Any]:
        """Load and parse the YAML registry file."""
        if not REGISTRY_PATH.exists():
            raise FileNotFoundError(
                f"Prompt registry not found at {REGISTRY_PATH}. "
                "Run prompt library setup first."
            )
        with open(REGISTRY_PATH, encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _find_entry(self, prompt_id: str) -> dict[str, Any]:
        """Look up a prompt entry by ID in the registry."""
        for entry in self.registry.get("prompts", []):
            if entry["id"] == prompt_id:
                return entry
        available = [p["id"] for p in self.registry.get("prompts", [])]
        raise KeyError(
            f"Prompt '{prompt_id}' not found in registry. "
            f"Available: {available}"
        )


# ── CLI Entry Point ───────────────────────────────────────────

def main() -> None:
    """CLI for browsing the prompt library."""
    import sys

    lib = PromptLibrary()

    if len(sys.argv) < 2:
        lib.print_catalog()
        return

    command = sys.argv[1]

    if command == "list":
        category = sys.argv[2] if len(sys.argv) > 2 else None
        lib.print_catalog(category)
    elif command == "info":
        if len(sys.argv) < 3:
            print("Usage: python prompt_library.py info <prompt-id>")
            return
        lib.print_info(sys.argv[2])
    elif command == "render":
        if len(sys.argv) < 3:
            print("Usage: python prompt_library.py render <prompt-id> [key=value ...]")
            return
        prompt_id = sys.argv[2]
        variables = {}
        for arg in sys.argv[3:]:
            if "=" in arg:
                k, v = arg.split("=", 1)
                variables[k] = v
        rendered = lib.render(prompt_id, **variables)
        print(rendered)
    elif command == "categories":
        cats = lib.get_categories()
        for slug, info in cats.items():
            desc = info if isinstance(info, str) else info.get("description", "")
            print(f"  {slug:<12} {desc}")
    else:
        print(f"Unknown command: {command}")
        print("Commands: list [category], info <id>, render <id> [key=value ...], categories")


if __name__ == "__main__":
    main()
