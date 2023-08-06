# test_fzf.py

import pytest
from pyselector.menus.fzf import Fzf


@pytest.fixture
def fzf() -> Fzf:
    return Fzf()


def test_check_command(fzf) -> None:
    assert "fzf" in fzf.command


def test_build_command(fzf) -> None:
    alt_n = fzf.keybind.add(
        key="alt-n",
        description="do something...",
        callback=lambda: None,
        hidden=False,
    )

    args = fzf._build_command(
        case_sensitive=True,
        multi_select=False,
        prompt="Testing>",
        mesg="Testing...",
        cycle=True,
        preview=True,
    )

    assert "--prompt" in args
    assert "--header" in args
    assert "--cycle" in args
    assert f"--bind={alt_n.bind}:" in args
    assert "--no-preview" not in args

    with pytest.warns(UserWarning):
        other_args = fzf._build_command(
            case_sensitive=True,
            multi_select=True,
            prompt="Testing>",
            preview=False,
            invalid_arg=True,
        )

        assert "--no-preview" in other_args
        assert "--multi" in other_args
