"""Tests for nanobot/skills/english-train/scripts/lint_round_references.py.

The skill directory is hyphenated (`english-train`), so it is not importable as
a regular Python package. We invoke the script as a subprocess, matching the
pattern in test_lint_topics_context.py.

The lint script accepts a <skill-dir> argument and scans:
  <skill-dir>/SKILL.md
  <skill-dir>/references/feedback-format.md
  <skill-dir>/references/topics-context/*.md

For fixture-based tests we build a minimal skill-dir layout in tmp_path so the
script has something to scan without pulling in unrelated real files.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LINT_SCRIPT = (
    REPO_ROOT
    / "nanobot"
    / "skills"
    / "english-train"
    / "scripts"
    / "lint_round_references.py"
)
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "english-train" / "round-references"
REAL_SKILL_DIR = REPO_ROOT / "nanobot" / "skills" / "english-train"


def run_lint(skill_dir: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(LINT_SCRIPT), str(skill_dir)],
        capture_output=True,
        text=True,
    )


def _make_skill_dir(tmp_path: Path, skill_md: Path | None = None) -> Path:
    """Scaffold a minimal skill-dir layout under tmp_path.

    Copies `skill_md` as SKILL.md if provided; otherwise creates a clean stub.
    Creates empty references/feedback-format.md and references/topics-context/
    so the script can always find its targets.
    """
    (tmp_path / "references" / "topics-context").mkdir(parents=True)
    (tmp_path / "references" / "feedback-format.md").write_text("# Feedback Format\n")
    if skill_md is not None:
        shutil.copy(skill_md, tmp_path / "SKILL.md")
    else:
        (tmp_path / "SKILL.md").write_text("# SKILL\n")
    return tmp_path


# ---------------------------------------------------------------------------
# Positive cases
# ---------------------------------------------------------------------------


def test_real_skill_passes() -> None:
    """The actual skill dir must be clean — no banned patterns outside scoped sections."""
    result = run_lint(REAL_SKILL_DIR)
    assert result.returncode == 0, result.stdout + result.stderr


def test_round5_in_concept_explanation_passes(tmp_path: Path) -> None:
    skill_dir = _make_skill_dir(
        tmp_path, FIXTURES / "round5-in-concept-explanation.md"
    )
    result = run_lint(skill_dir)
    assert result.returncode == 0, result.stdout + result.stderr


def test_round5_in_comparison_passes(tmp_path: Path) -> None:
    skill_dir = _make_skill_dir(tmp_path, FIXTURES / "round5-in-comparison.md")
    result = run_lint(skill_dir)
    assert result.returncode == 0, result.stdout + result.stderr


# ---------------------------------------------------------------------------
# Negative cases — each fixture is isolated in its own tmp dir
# ---------------------------------------------------------------------------


def test_round5_in_general_prose_fails(tmp_path: Path) -> None:
    skill_dir = _make_skill_dir(tmp_path, FIXTURES / "round5-general-prose.md")
    result = run_lint(skill_dir)
    assert result.returncode == 1
    assert "forbidden pattern" in result.stdout


def test_5_round_pattern_fails(tmp_path: Path) -> None:
    skill_dir = _make_skill_dir(tmp_path, FIXTURES / "5-round-general-prose.md")
    result = run_lint(skill_dir)
    assert result.returncode == 1
    assert "forbidden pattern" in result.stdout


def test_after_round5_fails(tmp_path: Path) -> None:
    skill_dir = _make_skill_dir(tmp_path, FIXTURES / "after-round5-general-prose.md")
    result = run_lint(skill_dir)
    assert result.returncode == 1
    assert "forbidden pattern" in result.stdout


def test_exactly_5_rounds_fails(tmp_path: Path) -> None:
    skill_dir = _make_skill_dir(
        tmp_path, FIXTURES / "exactly-5-rounds-general-prose.md"
    )
    result = run_lint(skill_dir)
    assert result.returncode == 1
    assert "forbidden pattern" in result.stdout


def test_round_5_after_nonscoped_h2_fails(tmp_path: Path) -> None:
    """A `## Some Other Section` heading resets scope; Round 5 under it must fail."""
    skill_dir = _make_skill_dir(tmp_path, FIXTURES / "round5-after-nonscoped-h2.md")
    result = run_lint(skill_dir)
    assert result.returncode == 1
    assert "forbidden pattern" in result.stdout
