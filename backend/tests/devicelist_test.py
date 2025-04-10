from config import microlabConfig
microlabConfig.validate_config()

from hardware.devicelist import validateConfiguration, sort_device_configs
import pytest

from localization import load_translation


def test_detects_deplicate_ids():
    t=load_translation()
    
    devices = [
        {
            "id": "1"
        },
        {
            "id": "1"
        },
    ]
    with pytest.raises(Exception, match=t['duplicate-device-id-wo-format']):
        res = validateConfiguration(devices)


def test_detects_simple_circular_dependencies():
    t=load_translation()
  
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
    with pytest.raises(Exception, match=t['circular-dependency']):
        res = validateConfiguration(devices)


def test_detects_complex_circular_dependencies():
    t=load_translation()
    
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
    with pytest.raises(Exception, match=t['circular-dependency']):
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
    t=load-translation()
    
    devices = [
        {
            "id": "1",
            "dependencies": ["2"]
        },
    ]
    with pytest.raises(Exception, match=t['missing-config-wo-format']):
        res = validateConfiguration(devices)


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

