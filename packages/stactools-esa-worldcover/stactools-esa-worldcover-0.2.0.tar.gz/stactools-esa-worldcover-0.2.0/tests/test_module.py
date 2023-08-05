import stactools.esa_worldcover


def test_version() -> None:
    assert stactools.esa_worldcover.__version__ is not None
