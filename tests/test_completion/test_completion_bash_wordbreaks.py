import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from ..utils import needs_bash
from . import colon_example as mod


def _extract_complete_var(script: str) -> str:
    match = re.search(r"(\_[A-Z0-9_.]+_COMPLETE)=complete_bash", script)
    assert match is not None, "bash completion script missing complete_bash env var"
    return match.group(1)


def _bash_completion_reply(
    *,
    python_cmd: str,
    complete_var: str,
    comp_line: str,
) -> str:
    bash = shutil.which("bash")
    if bash is None:
        raise RuntimeError("bash not found")

    with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as handle:
        handle.write(
            f"""
COMP_LINE={comp_line!r}
COMP_POINT=${{#COMP_LINE}}
COMP_WORDBREAKS=$' \\t\\n\"\\'@><=;|&(:'
_colon_examplepy_completion() {{
    local __line=${{COMP_LINE:0:COMP_POINT}}
    local -a __words
    read -ra __words <<< "$__line"
    local __cword=${{#__words[@]}}
    [[ $__line != *[[:space:]] ]] && __cword=$((__cword - 1))
    local __full=${{__words[__cword]-}}

    local IFS=$'\\n'
    local -a __raw
    __raw=( $( env COMP_WORDS="${{__words[*]}}" \\
                   COMP_CWORD=$__cword \\
                   {complete_var}=complete_bash {python_cmd} ) ) || true

    local __wordbreaks="$COMP_WORDBREAKS"
    if [[ -z "$__wordbreaks" ]]; then
        __wordbreaks=$' \\t\\n\"\\'@><=;|&(:'
    fi
    local __cur=${{__full##*[$__wordbreaks]}}
    local __strip=$(( ${{#__full}} - ${{#__cur}} ))
    COMPREPLY=()
    local __c
    for __c in "${{__raw[@]}}"; do
        COMPREPLY+=( "${{__c:__strip}}" )
    done
    return 0
}}
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
    assert "__wordbreaks" in show.stdout or "COMP_WORDBREAKS" in show.stdout

    complete_var = _extract_complete_var(show.stdout)
    python_cmd = f"{sys.executable} -m coverage run {Path(mod.__file__).as_posix()}"
    reply = _bash_completion_reply(
        python_cmd=python_cmd,
        complete_var=complete_var,
        comp_line="colon_example.py --name alpine:l",
    )
    assert "latest" in reply.splitlines()
    assert "alpine:latest" not in reply
