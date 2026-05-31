"""Integration tests: run all active lints together and verify scope isolation.

These tests answer two questions:
1. Do all lints pass clean on the real skill files? (regression guard)
2. Is the a-stuffing anti-abuse violation scoped to T9 only — not caught by T10/T11?
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = REPO_ROOT / "nanobot" / "skills" / "english-train"
SCRIPTS = SKILL_DIR / "scripts"

LINT_T9 = SCRIPTS / "lint_feedback_format.py"
LINT_T10 = SCRIPTS / "lint_round_references.py"
LINT_T11 = SCRIPTS / "lint_anti_backdoor.py"

ANTI_ABUSE_FIXTURES = REPO_ROOT / "tests" / "fixtures" / "english-train" / "anti-abuse"


def _run(script: Path, target: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(script), str(target)],
        capture_output=True,
        text=True,
    )


def _make_skill_dir(tmp_path: Path, skill_md_content: str = "# SKILL\n") -> Path:
    refs = tmp_path / "references"
    refs.mkdir(parents=True)
    (refs / "feedback-format.md").write_text("# Feedback Format\n")
    (tmp_path / "SKILL.md").write_text(skill_md_content)
    return tmp_path


# ---------------------------------------------------------------------------
# Real skill dir — all lints must pass
# ---------------------------------------------------------------------------


def test_all_lints_pass_on_real_skill() -> None:
    """Regression guard: all lints exit 0 on the current real skill files."""
    for lint_script in [LINT_T9, LINT_T10, LINT_T11]:
        result = _run(lint_script, SKILL_DIR)
        assert result.returncode == 0, (
            f"{lint_script.name} failed on real skill dir:\n"
            f"{result.stdout}{result.stderr}"
        )


# ---------------------------------------------------------------------------
# a-stuffing fixture — T9 catches it; T10 and T11 do not
# ---------------------------------------------------------------------------


def test_t9_catches_a_stuffing(tmp_path: Path) -> None:
    """T9 must exit 1 on the a-stuffing anti-abuse fixture (5-bullet Try-to-use block)."""
    skill_dir = _make_skill_dir(
        tmp_path, (ANTI_ABUSE_FIXTURES / "a-stuffing.md").read_text()
    )
    result = _run(LINT_T9, skill_dir)
    assert result.returncode == 1
    output = result.stdout + result.stderr
    assert "5" in output or "max 2" in output


def test_a_stuffing_not_caught_by_t10(tmp_path: Path) -> None:
    """T10 exits 0 on a-stuffing: no round-number patterns present."""
    skill_dir = _make_skill_dir(
        tmp_path, (ANTI_ABUSE_FIXTURES / "a-stuffing.md").read_text()
    )
    result = _run(LINT_T10, skill_dir)
    assert result.returncode == 0, result.stdout + result.stderr


def test_a_stuffing_not_caught_by_t11(tmp_path: Path) -> None:
    """T11 exits 0 on a-stuffing: no backdoor phrases present."""
    skill_dir = _make_skill_dir(
        tmp_path, (ANTI_ABUSE_FIXTURES / "a-stuffing.md").read_text()
    )
    result = _run(LINT_T11, skill_dir)
    assert result.returncode == 0, result.stdout + result.stderr
