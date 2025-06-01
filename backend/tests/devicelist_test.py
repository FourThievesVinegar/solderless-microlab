from config import microlab_config
microlab_config.validate_config()

from hardware.devicelist import validateConfiguration, sort_device_configs
import pytest


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
        validateConfiguration(devices)


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
        validateConfiguration(devices)


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
        validateConfiguration(devices)


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
    try:
        validateConfiguration(devices)
        assert True
    except Exception:
        assert False


def test_detects_missing_dependencies():
    devices = [
        {
            "id": "1",
            "dependencies": ["2"]
        },
    ]
    with pytest.raises(Exception, match='Missing hardware configuration for dependency'):
        validateConfiguration(devices)


def test_sort_device_configs_sorts_by_dependencies():
    devices = [
        {
            "id": "1",
            "dependencies": ["2"]
        },
        {
            "id": "2",
        },
    ]

    assert sort_device_configs(devices) == [
        {
            "id": "2",
        },
        {
            "id": "1",
            "dependencies": ["2"]
        },
    ]
