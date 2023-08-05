from pystac.utils import str_to_datetime

from stactools.esa_worldcover import stac
from tests import test_data


def test_create_2020_item() -> None:
    href = test_data.get_path(
        "data-files/ESA_WorldCover_10m_2020_v100_N00E006/"
        "ESA_WorldCover_10m_2020_v100_N00E006_Map.tif"
    )
    item = stac.create_item(href)
    item.validate()

    assert item.id == "ESA_WorldCover_10m_2020_v100_N00E006"

    assert len(item.assets) == 1
    assert item.properties.get("proj:transform", None) is not None
    assert item.properties.get("proj:shape", None) is not None

    assert item.common_metadata.start_datetime == str_to_datetime(
        "2020-01-01T00:00:00Z"
    )
    assert item.common_metadata.end_datetime == str_to_datetime("2020-12-31T23:59:59Z")
    assert item.properties["esa_worldcover:product_version"] == "1.0.0"

    item = stac.create_item(href, include_quality_asset=True)
    item.validate()

    assert len(item.assets) == 2
    assert item.properties.get("proj:transform", None) is None
    assert item.properties.get("proj:shape", None) is None


def test_create_2021_item() -> None:
    href = test_data.get_path(
        "data-files/ESA_WorldCover_10m_2021_v200_N00E006/"
        "ESA_WorldCover_10m_2021_v200_N00E006_Map.tif"
    )
    item = stac.create_item(href)
    item.validate()

    assert item.id == "ESA_WorldCover_10m_2021_v200_N00E006"

    assert len(item.assets) == 1
    assert item.properties.get("proj:transform", None) is not None
    assert item.properties.get("proj:shape", None) is not None

    assert item.common_metadata.start_datetime == str_to_datetime(
        "2021-01-01T00:00:00Z"
    )
    assert item.common_metadata.end_datetime == str_to_datetime("2021-12-31T23:59:59Z")
    assert item.properties["esa_worldcover:product_version"] == "2.0.0"

    item = stac.create_item(href, include_quality_asset=True)
    item.validate()

    assert len(item.assets) == 2
    assert item.properties.get("proj:transform", None) is None
    assert item.properties.get("proj:shape", None) is None


def test_read_href_modifier() -> None:
    href = test_data.get_path(
        "data-files/ESA_WorldCover_10m_2020_v100_N00E006/ESA_WorldCover_10m_2020_v100_N00E006_Map.tif"  # noqa
    )
    did_it = False

    def read_href_modifier(href: str) -> str:
        nonlocal did_it
        did_it = True
        return href

    _ = stac.create_item(href, read_href_modifier=read_href_modifier)
    assert did_it


def test_create_collection() -> None:
    collection = stac.create_collection("esa-worldcover")
    collection.validate()

    collection.set_self_href("")
    assert collection.id == "esa-worldcover"
    assert len(collection.summaries.lists["esa_worldcover:product_version"]) == 2
    assert collection.extent.temporal.intervals[0] == [
        str_to_datetime("2020-01-01T00:00:00Z"),
        str_to_datetime("2021-12-31T23:59:59Z"),
    ]
