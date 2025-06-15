from config import microlab_config
microlab_config.validate_config()

from hardware.devicelist import validate_configuration, sort_device_configs
import pytest


def test_detects_deplicate_ids():
    device_definitions = [
        {
            'id': '1'
        },
        {
            'id': '1'
        },
    ]
    with pytest.raises(Exception, match='Duplicate device id'):
        validate_configuration(device_definitions)


def test_detects_simple_circular_dependencies():
    device_definitions = [
        {
            'id': '1',
            'dependencies': ['2']
        },
        {
            'id': '2',
            'dependencies': ['1']
        },
    ]
    with pytest.raises(Exception, match='Circular dependency'):
        validate_configuration(device_definitions)


def test_detects_complex_circular_dependencies():
    device_definitions = [
        {
            'id': '4',
            'dependencies': ['1']
        },
        {
            'id': '2',
            'dependencies': ['3']
        },
        {
            'id': '1',
            'dependencies': ['2']
        },
        {
            'id': '3',
            'dependencies': ['4']
        },
    ]
    with pytest.raises(Exception, match='Circular dependency'):
        validate_configuration(device_definitions)


def test_accepts_simple_valid_config():
    device_definitions = [
        {
            'id': '1'
        },
        {
            'id': '2',
            'dependencies': ['1']
        },
        {
            'id': '3',
            'dependencies': ['2']
        },
        {
            'id': '4',
            'dependencies': ['3']
        },
    ]
    try:
        validate_configuration(device_definitions)
        assert True
    except Exception:
        assert False


def test_detects_missing_dependencies():
    device_definitions = [
        {
            'id': '1',
            'dependencies': ['2']
        },
    ]
    with pytest.raises(Exception, match='Missing hardware configuration for dependency'):
        validate_configuration(device_definitions)


def test_sort_device_configs_sorts_by_dependencies():
    device_definitions = [
        {
            'id': '1',
            'dependencies': ['2']
        },
        {
            'id': '2',
        },
    ]

    assert sort_device_configs(device_definitions) == [
        {
            'id': '2',
        },
        {
            'id': '1',
            'dependencies': ['2']
        },
    ]


# if __name__ == '__main__':
#     import sys
#     sys.exit(pytest.main([__file__]))
