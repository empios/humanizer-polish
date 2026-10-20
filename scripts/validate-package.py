#!/usr/bin/env python3
"""Check humanizer-polish package files without external dependencies.

Adapted from blader/humanizer (MIT). Messages stay in English, like the original,
so contributors outside Poland can read them.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = "humanizer-polish"


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        raise SystemExit(f"Cannot read {path.relative_to(ROOT)}: {error}") from None


def load_json(path: Path) -> dict:
    try:
        return json.loads(read(path))
    except json.JSONDecodeError as error:
        raise SystemExit(f"Fix the JSON in {path.relative_to(ROOT)}: {error}") from None


def require(match: re.Match[str] | None, message: str) -> re.Match[str]:
    if match is None:
        raise SystemExit(message)
    return match


SKILL_PATH = ROOT / "SKILL.md"
SKILL = read(SKILL_PATH)
README = read(ROOT / "README.md")
CHANGELOG = read(ROOT / "CHANGELOG.md")
PLUGIN = load_json(ROOT / ".claude-plugin" / "plugin.json")
MARKETPLACE = load_json(ROOT / ".claude-plugin" / "marketplace.json")

yaml_metadata = require(
    re.match(r"\A---\n(.*?)\n---\n", SKILL, re.DOTALL), "SKILL.md must begin with YAML metadata"
).group(1)
for unsupported in ("version:", "compatibility:", "allowed-tools:"):
    if re.search(rf"(?m)^{re.escape(unsupported)}", yaml_metadata):
        raise SystemExit(f"Remove unsupported YAML field: {unsupported[:-1]}")
if not re.search(rf"(?m)^name: {re.escape(NAME)}$", yaml_metadata):
    raise SystemExit(f"Set name: {NAME} in SKILL.md")

skill_version = require(
    re.search(r'(?m)^\s+version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)["\']?\s*$', yaml_metadata),
    "Add metadata.version to SKILL.md as a three-part version",
).group(1)
changelog_version = require(
    re.search(r"(?m)^## ([0-9]+\.[0-9]+\.[0-9]+)$", CHANGELOG), "Add a version heading to CHANGELOG.md"
).group(1)
versions = {
    skill_version,
    changelog_version,
    str(PLUGIN.get("version", "")),
    *(str(p.get("version", "")) for p in MARKETPLACE.get("plugins", [])),
}
if len(versions) != 1:
    raise SystemExit(f"Use one package version in all files: {sorted(versions)}")

skill_files = {path.relative_to(ROOT) for path in ROOT.rglob("SKILL.md")}
if SKILL_PATH.is_symlink() or skill_files != {Path("SKILL.md")}:
    raise SystemExit("Keep one regular SKILL.md at the repo root")
if PLUGIN.get("name") != NAME or PLUGIN.get("skills") != ["./"]:
    raise SystemExit(f"Name the Claude plugin {NAME} and point its skill loader at the repo root")

description = " ".join(
    require(
        re.search(r"(?m)^description: \|\n((?:  .*\n)+)", yaml_metadata + "\n"),
        "Write the SKILL.md description as an indented block",
    ).group(1).split()
)
manifest_descriptions = {
    str(PLUGIN.get("description", "")),
    *(str(p.get("description", "")) for p in MARKETPLACE.get("plugins", [])),
}
if len(manifest_descriptions) != 1 or not description.startswith(next(iter(manifest_descriptions))):
    raise SystemExit(
        "Use the first sentence of the SKILL.md description in every plugin manifest: "
        f"{sorted(manifest_descriptions)}"
    )

patterns = {int(n): name for n, name in re.findall(r"(?m)^### ([0-9]+)\. (.+)$", SKILL)}
numbers = list(patterns)
count = len(numbers)
if count == 0 or numbers != list(range(1, count + 1)):
    raise SystemExit(f"Number SKILL.md patterns from 1 upward without gaps: {numbers}")

readme_patterns = {int(n): name for n, name in re.findall(r"(?m)^\| ([0-9]+) \| \*\*(.+?)\*\*", README)}
if sorted(readme_patterns) != numbers:
    raise SystemExit(f"List patterns 1 through {count} once each in the README tables: {sorted(readme_patterns)}")
renamed = [f"{n}: {readme_patterns[n]!r} should be {name!r}" for n, name in patterns.items()
           if readme_patterns[n] != name]
if renamed:
    raise SystemExit("Match the README pattern names to SKILL.md: " + "; ".join(renamed))
if f"## {count} wzorców" not in README:
    raise SystemExit(f"Title the README pattern section '{count} wzorców'")

references = sorted({int(n) for n in re.findall(r"§([0-9]+)", SKILL)})
missing = [n for n in references if not 1 <= n <= count]
if missing:
    raise SystemExit(f"Point every SKILL.md section reference at a pattern from 1 to {count}: {missing}")

for path in sorted(set(re.findall(r"`((?:scripts|references)/[^`\s]+)`", SKILL))):
    if not (ROOT / path).is_file():
        raise SystemExit(f"SKILL.md names a file that does not exist: {path}")

# The skill must follow its own dash rule (§8) outside the section that describes it.
section_8 = require(re.search(r"(?ms)^### 8\. .*?(?=^### 9\. )", SKILL), "Keep pattern 8 before pattern 9")
outside = SKILL.replace(section_8.group(0), "")
if "—" in outside or "–" in outside or re.search(r"\s--\s", outside):
    raise SystemExit("SKILL.md uses an em dash, an en dash or a double hyphen outside pattern 8; use an ASCII hyphen")
# Polish quotes open with „ and close with ”; an English opening “ belongs only in pattern 20.
section_20 = require(re.search(r"(?ms)^### 20\. .*?(?=^## )", SKILL), "Keep pattern 20 before the next section")
if "“" in SKILL.replace(section_20.group(0), ""):
    raise SystemExit("SKILL.md uses an English opening quote “ outside pattern 20; use „…”")

words = len(SKILL.split())
if words > 5500:
    raise SystemExit(f"Keep SKILL.md at 5,500 words or fewer; it has {words}")

print(f"humanizer-polish v{skill_version} is valid: {count} patterns, {words} words")
