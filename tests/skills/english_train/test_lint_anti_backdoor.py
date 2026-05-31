"""Tests for nanobot/skills/english-train/scripts/lint_anti_backdoor.py.

The skill directory is hyphenated (`english-train`), so it is not importable as
a regular Python package. We invoke the script as a subprocess, matching the
pattern used by test_lint_feedback_format.py and test_lint_topics_context.py.
"""
from __future__ import annotations

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
    / "lint_anti_backdoor.py"
)
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "english-train" / "anti-backdoor"
REAL_SKILL_DIR = REPO_ROOT / "nanobot" / "skills" / "english-train"


def run_lint(target_dir: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(LINT_SCRIPT), str(target_dir)],
        capture_output=True,
        text=True,
    )


# ---------------------------------------------------------------------------
# Real skill dir — must pass (no banned phrases in current files)
# ---------------------------------------------------------------------------


def test_real_skill_passes() -> None:
    result = run_lint(REAL_SKILL_DIR)
    assert result.returncode == 0, result.stdout + result.stderr


# ---------------------------------------------------------------------------
# Per-pattern fixtures — each banned phrase triggers exit 1
# ---------------------------------------------------------------------------


def test_pattern1_didnt_use_suggested_pattern_fails(tmp_path: Path) -> None:
    # "didn't use the suggested pattern"
    refs = tmp_path / "references"
    refs.mkdir()
    (refs / "feedback-format.md").write_text(
        (FIXTURES / "pattern-1-didnt-use.md").read_text()
    )
    result = run_lint(tmp_path)
    assert result.returncode == 1
    assert "forbidden phrase" in result.stdout


def test_pattern2_should_have_used_fails(tmp_path: Path) -> None:
    # "should have used the suggested template"
    refs = tmp_path / "references"
    refs.mkdir()
    (refs / "feedback-format.md").write_text(
        (FIXTURES / "pattern-2-should-have-used.md").read_text()
    )
    result = run_lint(tmp_path)
    assert result.returncode == 1
    assert "forbidden phrase" in result.stdout


def test_pattern3_pattern_adherence_fails(tmp_path: Path) -> None:
    # "pattern adherence"
    refs = tmp_path / "references"
    refs.mkdir()
    (refs / "scoring.md").write_text(
        (FIXTURES / "pattern-3-adherence.md").read_text()
    )
    result = run_lint(tmp_path)
    assert result.returncode == 1
    assert "forbidden phrase" in result.stdout


def test_pattern4_failed_to_use_fails(tmp_path: Path) -> None:
    # "failed to use the template"
    (tmp_path / "SKILL.md").write_text(
        (FIXTURES / "pattern-4-failed-to-use.md").read_text()
    )
    result = run_lint(tmp_path)
    assert result.returncode == 1
    assert "forbidden phrase" in result.stdout


def test_pattern5_must_use_fails(tmp_path: Path) -> None:
    # "must use the recommended pattern"
    (tmp_path / "SKILL.md").write_text(
        (FIXTURES / "pattern-5-must-use.md").read_text()
    )
    result = run_lint(tmp_path)
    assert result.returncode == 1
    assert "forbidden phrase" in result.stdout


# ---------------------------------------------------------------------------
# Multiple violations are all reported
# ---------------------------------------------------------------------------


def test_multiple_violations_reports_all(tmp_path: Path) -> None:
    # Contains both "didn't use the suggested pattern" and "pattern adherence"
    refs = tmp_path / "references"
    refs.mkdir()
    (refs / "feedback-format.md").write_text(
        (FIXTURES / "multiple-violations.md").read_text()
    )
    result = run_lint(tmp_path)
    assert result.returncode == 1
    # Both violations should appear in output
    lines = [ln for ln in result.stdout.splitlines() if "forbidden phrase" in ln]
    assert len(lines) >= 2


# ---------------------------------------------------------------------------
# Case-insensitive matching
# ---------------------------------------------------------------------------


def test_case_insensitive(tmp_path: Path) -> None:
    # "Pattern Adherence" (capital P, capital A) must also be caught
    refs = tmp_path / "references"
    refs.mkdir()
    (refs / "scoring.md").write_text(
        (FIXTURES / "case-insensitive.md").read_text()
    )
    result = run_lint(tmp_path)
    assert result.returncode == 1
    assert "forbidden phrase" in result.stdout
