import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

from . import colon_example as mod

from ..utils import needs_bash


def _bash_completion_reply(
  script: str,
  *,
  wrapper_dir: Path,
  comp_line: str,
  comp_words: str,
  comp_cword: str,
) -> str:
  bash = shutil.which("bash")
  if bash is None:
    raise RuntimeError("bash not found")
  with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as handle:
    handle.write(
      f"""
set -euo pipefail
export PATH={wrapper_dir}:{os.environ.get("PATH", "")}
{script}
COMP_LINE={comp_line!r}
COMP_POINT=${{#COMP_LINE}}
COMP_WORDS=({comp_words})
COMP_CWORD={comp_cword}
_colon_examplepy_completion colon_example.py
printf '%s\\n' "${{COMPREPLY[@]}}"
"""
    )
    path = handle.name
  try:
    result = subprocess.run(
      [bash, "--norc", path],
      capture_output=True,
      encoding="utf-8",
      env={**os.environ, "PYTHONPATH": os.pathsep.join(sys.path)},
    )
  finally:
    Path(path).unlink(missing_ok=True)
  assert result.returncode == 0, result.stderr
  return result.stdout


@needs_bash
def test_bash_completion_script_handles_comp_wordbreaks_colon() -> None:
  show = subprocess.run(
    [
      sys.executable,
      "-m",
      "coverage",
      "run",
      mod.__file__,
      "--show-completion",
      "bash",
    ],
    capture_output=True,
    encoding="utf-8",
    env={
      **os.environ,
      "_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION": "True",
    },
  )
  assert show.returncode == 0
  assert "COMP_LINE" in show.stdout
  assert "COMP_WORDBREAKS" in show.stdout

  with tempfile.TemporaryDirectory() as tmp:
    wrapper_dir = Path(tmp)
    wrapper = wrapper_dir / "colon_example.py"
    wrapper.write_text(
      f"#!/bin/sh\nexec {sys.executable} -m coverage run {mod.__file__} \"$@\"\n"
    )
    wrapper.chmod(wrapper.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    reply = _bash_completion_reply(
      show.stdout,
      wrapper_dir=wrapper_dir,
      comp_line="colon_example.py --name alpine:l",
      comp_words="colon_example.py --name : l",
      comp_cword="3",
    )
  assert "latest" in reply.splitlines()
  assert "alpine:latest" not in reply
