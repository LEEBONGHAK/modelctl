from modelctl_core.plugins.registry import (
    PluginRegistry,
)


def test_registry():
    registry = PluginRegistry()
    registry.discover()

    assert isinstance(
        registry.list_providers(),
        list,
    )
