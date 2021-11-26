import pytest
from filelock import FileLock


@pytest.fixture
def bashrc_lock():
    with FileLock(".bachrc.lock"):
        yield


@pytest.fixture
def zshrc_lock():
    with FileLock(".zsh.lock"):
        yield


@pytest.fixture
def fish_config_lock():
    with FileLock(".fish.lock"):
        yield


@pytest.fixture
def powershell_profile_lock():
    with FileLock(".powershell.lock"):
        yield
