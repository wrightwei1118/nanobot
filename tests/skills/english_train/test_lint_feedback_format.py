"""Tests for nanobot/skills/english-train/scripts/lint_feedback_format.py.

The skill directory is hyphenated (`english-train`), so it is not importable as
a regular Python package. We invoke the script as a subprocess, matching the
pattern used by test_lint_topics_context.py.
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
    / "lint_feedback_format.py"
)
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "english-train" / "feedback-format"
ANTI_ABUSE_FIXTURES = REPO_ROOT / "tests" / "fixtures" / "english-train" / "anti-abuse"
REAL_SKILL_DIR = REPO_ROOT / "nanobot" / "skills" / "english-train"


def run_lint(target_dir: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(LINT_SCRIPT), str(target_dir)],
        capture_output=True,
        text=True,
    )


# ---------------------------------------------------------------------------
# Real skill dir
# ---------------------------------------------------------------------------


def test_real_skill_passes() -> None:
    result = run_lint(REAL_SKILL_DIR)
    assert result.returncode == 0, result.stdout + result.stderr


# ---------------------------------------------------------------------------
# Anti-abuse fixture
# ---------------------------------------------------------------------------


def test_a_stuffing_fixture_fails(tmp_path: Path) -> None:
    shutil.copy(ANTI_ABUSE_FIXTURES / "a-stuffing.md", tmp_path / "a-stuffing.md")
    result = run_lint(tmp_path)
    assert result.returncode == 1
    output = result.stdout + result.stderr
    # Violation message must mention the count or the cap
    assert "5" in output or "max 2" in output


# ---------------------------------------------------------------------------
# Synthetic fixtures — positive cases
# ---------------------------------------------------------------------------


def test_two_bullets_passes(tmp_path: Path) -> None:
    shutil.copy(FIXTURES / "two-bullets.md", tmp_path / "two-bullets.md")
    result = run_lint(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr


def test_zero_bullets_passes(tmp_path: Path) -> None:
    shutil.copy(FIXTURES / "zero-bullets.md", tmp_path / "zero-bullets.md")
    result = run_lint(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr


def test_block_ends_on_blank_line(tmp_path: Path) -> None:
    # 5 total bullets but blank line breaks the block after bullet 2 → passes
    shutil.copy(FIXTURES / "blank-line-break.md", tmp_path / "blank-line-break.md")
    result = run_lint(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr


def test_block_ends_on_heading(tmp_path: Path) -> None:
    # 5 total bullets but ### heading breaks the block after bullet 2 → passes
    shutil.copy(FIXTURES / "heading-break.md", tmp_path / "heading-break.md")
    result = run_lint(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr


# ---------------------------------------------------------------------------
# Synthetic fixtures — negative cases
# ---------------------------------------------------------------------------


def test_three_bullets_fails(tmp_path: Path) -> None:
    shutil.copy(FIXTURES / "three-bullets.md", tmp_path / "three-bullets.md")
    result = run_lint(tmp_path)
    assert result.returncode == 1
    output = result.stdout + result.stderr
    assert "3" in output or "max 2" in output
