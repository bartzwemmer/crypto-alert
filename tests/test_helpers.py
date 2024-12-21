from pathlib import Path

import pytest

from helpers import read_config
from models import Config


def test_read_config():
    assert read_config(path=Path("./tests/test_config.yaml")) == {
        "deployment": {"slack_token": "my-token", "slack_channel": "my-channel"}
    }


def test_config():
    config = read_config()
    assert Config(**config)
