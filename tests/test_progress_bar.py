"""
Tests for the Progress bar functionality.
Created after vendoring Click to ensure test coverage is back up to 100%.
"""

import io
import shutil

import pytest
import typer
from typer import progressbar
from typer._click import _termui_impl
from typer.testing import CliRunner

runner = CliRunner()


def _fake_clock(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    clock = [0.0]
    monkeypatch.setattr(_termui_impl.time, "time", lambda: clock[0])
    return clock


def _pbar(**kw):
    return progressbar(file=kw.pop("file", io.StringIO()), **kw)


@pytest.mark.parametrize(
    ("iterable", "length", "hidden", "label", "expected_count"),
    [
        (["a", "b"], None, False, "Processing", 2),
        (None, 3, False, "Counting", 3),
        (["x", "y"], None, True, "Hidden", 2),
    ],
)
def test_progressbar(iterable, length, hidden, label, expected_count):
    app = typer.Typer()

    @app.command()
    def main():
        bar_out = io.StringIO()
        count = 0
        with progressbar(
            iterable, length=length, hidden=hidden, label=label, file=bar_out
        ) as bar:
            for _ in bar:
                count += 1
        typer.echo(f"count={count}")
        typer.echo(f"bar={bar_out.getvalue()!r}")

    result = runner.invoke(app, [])
    assert result.exit_code == 0, result.output
    assert f"count={expected_count}" in result.stdout
    assert (label in result.stdout) == (not hidden)


@pytest.mark.parametrize(
    ("label", "pbar_kw", "must_contain", "must_not_contain"),
    [
        pytest.param(
            "TTY",
            {
                "show_pos": True,
                "show_percent": True,
                "item_show_func": lambda item: f"item={item}",
            },
            ("TTY", "1/1", "100%", "item=x"),
            (),
        ),
        pytest.param(
            "HeurPct",
            {},
            ("HeurPct", "100%"),
            ("1/1",),
        ),
        pytest.param(
            "HeurPos",
            {"show_pos": True},
            ("HeurPos", "1/1"),
            ("100%",),
        ),
    ],
)
def test_progressbar_tty(
    monkeypatch, label: str, pbar_kw: dict, must_contain, must_not_contain
):
    monkeypatch.setattr(_termui_impl, "isatty", lambda f: True)
    _fake_clock(monkeypatch)

    app = typer.Typer()

    @app.command()
    def main():
        bar_out = io.StringIO()
        with progressbar(
            ["x"],
            label=label,
            file=bar_out,
            bar_template="%(label)s %(info)s",
            width=1,
            **pbar_kw,
        ) as bar:
            for _ in bar:
                pass
        typer.echo(bar_out.getvalue())

    result = runner.invoke(app, [])
    assert result.exit_code == 0, result.output
    for part in must_contain:
        assert part in result.stdout
    for part in must_not_contain:
        assert part not in result.stdout


def test_progressbar_tty_show_eta(monkeypatch):
    monkeypatch.setattr(_termui_impl, "isatty", lambda f: True)
    clock = _fake_clock(monkeypatch)
    clock[0] = 1_000.0

    app = typer.Typer()

    @app.command()
    def main():
        bar_out = io.StringIO()
        with progressbar(
            ["a", "b"],
            label="ETA",
            file=bar_out,
            show_pos=True,
            show_percent=False,
            show_eta=True,
            bar_template="%(label)s %(info)s",
            width=1,
        ) as bar:
            for i, _ in enumerate(bar):
                if i == 0:
                    clock[0] = 1_001.0
        typer.echo(bar_out.getvalue())

    result = runner.invoke(app, [])
    assert result.exit_code == 0, result.output
    for part in ("ETA", "1/2", "00:00:01"):
        assert part in result.stdout


def test_progressbar_autowidth(monkeypatch):
    monkeypatch.setattr(_termui_impl, "isatty", lambda f: True)
    call = [0]
    real_get_terminal_size = shutil.get_terminal_size

    def fake_get_terminal_size(*args, **kwargs):
        # Pytest (and others) call get_terminal_size(fallback=...); only stub no-arg calls
        if args or kwargs:
            return real_get_terminal_size(*args, **kwargs)
        col = 120 if call[0] == 0 else 40
        call[0] += 1
        return type("TS", (), {"columns": col, "lines": 24})()

    monkeypatch.setattr(shutil, "get_terminal_size", fake_get_terminal_size)

    state: dict[str, object] = {}

    app = typer.Typer()

    @app.command()
    def main():
        out = io.StringIO()
        with progressbar(["a", "b"], width=0, label="AW", file=out) as bar:
            state["autowidth"] = bar.autowidth
            for _ in bar:
                pass
        state["call_count"] = call[0]
        state["out"] = out.getvalue()
        typer.echo("done")

    result = runner.invoke(app, [])
    assert result.exit_code == 0, result.output
    assert state["autowidth"] is True
    assert state["call_count"] >= 2
    out = str(state["out"])
    assert "\r" in out and "AW" in out
    assert "0%" in out and "50%" in out and "100%" in out


def test_progress_bar_iter():
    not_entered = _pbar(iterable=[1, 2], length=2)
    with pytest.raises(RuntimeError, match="with block"):
        iter(not_entered)

    entered = _pbar(iterable=[10, 20], length=2)
    with entered:
        iterator = iter(entered)
        assert next(iterator) == 10
        assert next(entered) == 20
        with pytest.raises(StopIteration):
            next(iterator)


def test_progress_bar_time(monkeypatch):
    clock = _fake_clock(monkeypatch)
    state: dict[str, object] = {}
    clock[0] = 1_000.0

    app = typer.Typer()

    @app.command()
    def main():
        bar = _pbar(iterable=None, length=10)
        state["tpi0"] = bar.time_per_iteration
        clock[0] = 1_000.5
        bar.make_step(1)
        state["avg_after_one"] = list(bar.avg)
        state["tpi_after_one"] = bar.time_per_iteration
        clock[0] = 1_001.0
        bar.make_step(1)
        state["pos2"] = bar.pos
        state["avg2"] = list(bar.avg)
        state["tpi2"] = bar.time_per_iteration
        clock[0] = 1_002.0
        bar.make_step(1)
        state["avg3"] = list(bar.avg)
        state["tpi3"] = bar.time_per_iteration
        typer.echo("ok")

    result = runner.invoke(app, [])
    assert result.exit_code == 0, result.output
    assert state["tpi0"] == 0.0
    assert state["avg_after_one"] == [] and state["tpi_after_one"] == 0.0
    assert state["pos2"] == 2
    assert state["avg2"] == [(1_001.0 - 1_000.0) / 2.0]
    assert state["tpi2"] == pytest.approx(0.5)
    assert state["avg3"] == [0.5, (1_002.0 - 1_000.0) / 3.0]
    assert state["tpi3"] == pytest.approx(sum(state["avg3"]) / 2.0)  # type: ignore[arg-type]


def test_progress_bar_time_zero_steps(monkeypatch):
    clock = _fake_clock(monkeypatch)
    state: dict[str, object] = {}
    clock[0] = 2_000.0

    app = typer.Typer()

    @app.command()
    def main():
        bar = _pbar(iterable=None, length=3)
        clock[0] = 2_001.0
        bar.make_step(0)
        state["pos"] = bar.pos
        state["avg"] = list(bar.avg)
        state["tpi"] = bar.time_per_iteration
        typer.echo("ok")

    result = runner.invoke(app, [])
    assert result.exit_code == 0, result.output
    assert state["pos"] == 0
    assert state["avg"] == [1.0]
    assert state["tpi"] == pytest.approx(1.0)


def test_progress_bar_eta(monkeypatch):
    state: dict[str, object] = {}

    app = typer.Typer()

    @app.command()
    def main():
        state["eta0"] = _pbar(iterable=[1, 2], length=None).eta

        done = _pbar(iterable=None, length=5)
        done.pos, done.finished = 2, True
        state["eta_done"] = done.eta

        fresh = _pbar(iterable=None, length=5)
        state["eta_known_fresh"] = fresh.eta_known
        state["fmt_eta_fresh"] = fresh.format_eta()

        clock = _fake_clock(monkeypatch)
        clock[0] = 5_000.0
        bar = _pbar(iterable=None, length=10)
        clock[0] = 5_001.0
        bar.make_step(3)
        state["pos3"] = bar.pos
        state["eta_after"] = bar.eta
        state["tpi"] = bar.time_per_iteration

        cases_out = []
        for t0, t1, length, n_steps, _expected_fmt, expected_eta_int in (
            (9_000.0, 9_001.0, 10, 1, "00:00:09", None),
            (1_000.0, 100_000.0, 2, 1, "1d 03:30:00", 99_000),
        ):
            clock2 = _fake_clock(monkeypatch)
            clock2[0] = t0
            b = _pbar(iterable=None, length=length)
            clock2[0] = t1
            b.make_step(n_steps)
            cases_out.append(
                (
                    b.eta_known,
                    b.format_eta(),
                    int(b.eta) if expected_eta_int is not None else None,
                )
            )

        state["cases"] = cases_out

        clock3 = _fake_clock(monkeypatch)
        clock3[0] = 3_000.0
        b2 = _pbar(iterable=None, length=2)
        clock3[0] = 3_001.0
        b2.make_step(1)
        state["fmt_before_finish"] = b2.format_eta()
        b2.finish()
        state["fmt_after_finish"] = b2.format_eta()
        typer.echo("ok")

    result = runner.invoke(app, [])
    assert result.exit_code == 0, result.output
    assert state["eta0"] == 0.0
    assert state["eta_done"] == 0.0
    assert not state["eta_known_fresh"] and state["fmt_eta_fresh"] == ""
    assert state["pos3"] == 3
    assert state["eta_after"] == pytest.approx(state["tpi"] * (10 - 3))  # type: ignore[operator]

    (ek1, fmt1, ei1), (ek2, fmt2, ei2) = state["cases"]  # type: ignore[misc]
    assert ek1 and fmt1 == "00:00:09" and ei1 is None
    assert ek2 and fmt2 == "1d 03:30:00" and ei2 == 99_000

    assert state["fmt_before_finish"] != ""
    assert state["fmt_after_finish"] == ""


@pytest.mark.parametrize(
    ("width", "fill_char", "empty_char", "expected_bar", "finished", "sample_timing"),
    [
        pytest.param(4, "X", "-", "XXXX", True, False, id="finished"),
        pytest.param(4, "#", "-", "----", False, False, id="no_timing_yet"),
        pytest.param(5, "*", ".", None, False, True, id="indeterminate"),
    ],
)
def test_progress_bar_unknown_length(
    monkeypatch,
    width: int,
    fill_char: str,
    empty_char: str,
    expected_bar: str | None,
    finished: bool,
    sample_timing: bool,
):
    clock: list[float] | None = _fake_clock(monkeypatch) if sample_timing else None
    if clock is not None:
        clock[0] = 100.0

    state: dict[str, object] = {}

    class _IterableWithoutLength:
        def __iter__(self):
            return iter((1, 2, 3))

    app = typer.Typer()

    @app.command()
    def main():
        bar = _pbar(
            iterable=_IterableWithoutLength(),
            length=None,
            width=width,
            fill_char=fill_char,
            empty_char=empty_char,
        )
        assert bar.length is None

        if sample_timing:
            assert clock is not None
            clock[0] = 101.0
            bar.make_step(1)
            assert bar.time_per_iteration > 0
            rendered = bar.format_bar()
            assert len(rendered) == width
            assert rendered.count(fill_char) == 1
            assert rendered.count(empty_char) == width - 1
            state["branch"] = "sample_timing"
        elif finished:
            bar.finished = True
            state["bar"] = bar.format_bar()
            state["branch"] = "finished"
        else:
            assert bar.time_per_iteration == 0.0
            state["bar"] = bar.format_bar()
            state["branch"] = "no_timing"
        typer.echo("ok")

    result = runner.invoke(app, [])
    assert result.exit_code == 0, result.output
    if sample_timing:
        assert state["branch"] == "sample_timing"
    else:
        assert state["bar"] == expected_bar
