import os
import subprocess

from first_steps import tutorial001 as mod


def test_completion_install_source_bash():
    result = subprocess.run(
        ["coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "install-source_bash",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        'eval "$(_TUTORIAL001.PY_COMPLETE=source_bash tutorial001.py)"' in result.stdout
    )


def test_completion_install_source_zsh():
    result = subprocess.run(
        ["coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "install-source_zsh",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        'eval "$(_TUTORIAL001.PY_COMPLETE=source_szh tutorial001.py)"' in result.stdout
    )


def test_completion_install_source_fish():
    result = subprocess.run(
        ["coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "install-source_fish",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        "eval (env _TUTORIAL001.PY_COMPLETE=source_fish tutorial001.py)"
        in result.stdout
    )


def test_completion_install_source_powershell():
    result = subprocess.run(
        ["coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "install-source_powershell",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        "Register-ArgumentCompleter -Native -CommandName tutorial001.py -ScriptBlock $scriptblock"
        in result.stdout
    )


def test_completion_install_source_pwsh():
    result = subprocess.run(
        ["coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "install-source_pwsh",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        "Register-ArgumentCompleter -Native -CommandName tutorial001.py -ScriptBlock $scriptblock"
        in result.stdout
    )


def test_completion_install_source_noshell():
    result = subprocess.run(
        ["coverage", "run", mod.__file__],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "install-source_noshell",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "" in result.stdout
