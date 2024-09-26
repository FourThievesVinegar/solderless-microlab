from hardware.devicelist import validateConfiguration
import pytest
import yaml
import hardware.core
from unittest.mock import patch, MagicMock


def test_detects_deplicate_ids():
    devices = [
        {
            "id": "1"
        },
        {
            "id": "1"
        },
    ]
    with pytest.raises(Exception, match='Duplicate device id'):
        res = validateConfiguration(devices)


def test_detects_simple_circular_dependencies():
    devices = [
        {
            "id": "1",
            "dependencies": ["2"]
        },
        {
            "id": "2",
            "dependencies": ["1"]
        },
    ]
    with pytest.raises(Exception, match='Circular dependency'):
        res = validateConfiguration(devices)


def test_detects_complex_circular_dependencies():
    devices = [
        {
            "id": "4",
            "dependencies": ["1"]
        },
        {
            "id": "2",
            "dependencies": ["3"]
        },
        {
            "id": "1",
            "dependencies": ["2"]
        },
        {
            "id": "3",
            "dependencies": ["4"]
        },
    ]
    with pytest.raises(Exception, match='Circular dependency'):
        res = validateConfiguration(devices)


def test_accepts_simple_valid_config():
    devices = [
        {
            "id": "1"
        },
        {
            "id": "2",
            "dependencies": ["1"]
        },
        {
            "id": "3",
            "dependencies": ["2"]
        },
        {
            "id": "4",
            "dependencies": ["3"]
        },
    ]
    res = validateConfiguration(devices)
    assert res is False


def test_detects_missing_dependencies():
    devices = [
        {
            "id": "1",
            "dependencies": ["2"]
        },
    ]
    with pytest.raises(Exception, match='Missing hardware configuration for dependency'):
        res = validateConfiguration(devices)
