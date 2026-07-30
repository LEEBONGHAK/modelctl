from modelctl_core.container import Container


def test_container():
    container = Container()
    assert container.config
    assert container.providers