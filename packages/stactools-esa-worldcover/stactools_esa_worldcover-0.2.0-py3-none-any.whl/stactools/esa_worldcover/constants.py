from typing import Any, Dict

from pystac import (
    Extent,
    Link,
    MediaType,
    Provider,
    ProviderRole,
    SpatialExtent,
    Summaries,
    TemporalExtent,
)
from pystac.extensions.item_assets import AssetDefinition
from pystac.utils import str_to_datetime

ITEM_DESCRIPTION = "ESA WorldCover product at 10m resolution"
# Per the discussion in https://github.com/radiantearth/stac-spec/issues/216,
# the recommendation for multi-platform datasets is to include all platforms
# and use a string separator. The same logic is applied to the mission.
PLATFORM = "sentinel-1a, sentinel-1b, sentinel-2a, sentinel-2b"
MISSION = "sentinel-1, sentinel-2"
INSTRUMENTS = ["c-sar", "msi"]
EPSG = 4326
CLASSIFICATION_SCHEMA = (
    "https://stac-extensions.github.io/classification/v1.0.0/schema.json"
)

ASSET_PROPS: Dict[str, Any] = {
    "map": {
        "title": "Land Cover Classes",
        "description": (
            "Discrete classification according to the Land Cover Classification "
            "System scheme developed by the United Nations Food and Agriculture "
            "Organization"
        ),
        "roles": ["data"],
        "bands": [
            {
                "name": "Band1",
                "description": "Classification values",
                "nodata": 0,
                "sampling": "area",
                "data_type": "uint8",
                "spatial_resolution": 10,
            }
        ],
        "classes": [
            {"value": 10, "description": "Tree cover", "color-hint": "006400"},
            {"value": 20, "description": "Shrubland", "color-hint": "FFBB22"},
            {"value": 30, "description": "Grassland", "color-hint": "FFFF4C"},
            {"value": 40, "description": "Cropland", "color-hint": "F096FF"},
            {"value": 50, "description": "Built-up", "color-hint": "FA0000"},
            {
                "value": 60,
                "description": "Bare / sparse vegetation",
                "color-hint": "B4B4B4",
            },
            {"value": 70, "description": "Snow and ice", "color-hint": "F0F0F0"},
            {
                "value": 80,
                "description": "Permanent water bodies",
                "color-hint": "0064C8",
            },
            {"value": 90, "description": "Herbaceous wetland", "color-hint": "0096A0"},
            {"value": 95, "description": "Mangroves", "color-hint": "00CF75"},
            {"value": 100, "description": "Moss and lichen", "color-hint": "FAE6A0"},
        ],
    },
    "inputquality": {
        "title": "Classification Input Data Quality",
        "description": (
            "Per pixel quality indicator showing the quality of the input data."
        ),
        "roles": ["metadata"],
        "bands": [
            {
                "name": "Band1",
                "description": (
                    "Number of Sentinel-1 GAMMA0 observations used in the "
                    "classification workflow"
                ),
                "nodata": -1,
                "sampling": "area",
                "data_type": "int16",
                "spatial_resolution": 60,
            },
            {
                "name": "Band2",
                "description": (
                    "Number of Sentinel-2 L2A observations used in the "
                    "classification workflow"
                ),
                "nodata": -1,
                "sampling": "area",
                "data_type": "int16",
                "spatial_resolution": 60,
            },
            {
                "name": "Band3",
                "description": (
                    "Percentage (0-100) of invalid S2 observations discarded in "
                    "the classification workflow (after cloud and cloud shadow "
                    "filtering)"
                ),
                "nodata": -1,
                "sampling": "area",
                "data_type": "int16",
                "spatial_resolution": 60,
            },
        ],
    },
}

COLLECTION_TITLE = "ESA WorldCover"
COLLECTION_DESCRIPTION = (
    "Global land cover product at 10 meter resolution based on "
    "Sentinel-1 and Sentinel-2 data"
)
LICENSE = "CC-BY-4.0"
LICENSE_LINK = Link(
    rel="license",
    target="https://spdx.org/licenses/CC-BY-4.0.html",
    media_type=MediaType.HTML,
    title="Creative Commons Attribution 4.0 International License",
)
CITE_AS_LINK_2020 = Link(
    rel="cite-as",
    target="https://doi.org/10.5281/zenodo.5571936 ",
    media_type=MediaType.HTML,
    title="2020 Data DOI",
)
CITE_AS_LINK_2021 = Link(
    rel="cite-as",
    target="https://doi.org/10.5281/zenodo.7254221",
    media_type=MediaType.HTML,
    title="2021 Data DOI",
)
KEYWORDS = ["Global", "Land Cover", "Sentinel", "ESA"]
PROVIDERS = [
    Provider(
        name="ESA",
        roles=[ProviderRole.LICENSOR, ProviderRole.PRODUCER, ProviderRole.HOST],
        url="https://esa-worldcover.org",
    ),
    Provider(
        name="ESA WorldCover Consortium",
        description=(
            "The WorldCover product is developed by a consortium led by "
            "VITO Remote Sensing together with partners Brockmann Consult, "
            "CS SI, Gamma Remote Sensing AG, IIASA and Wageningen "
            "University"
        ),
        roles=[ProviderRole.PROCESSOR],
        url="https://esa-worldcover.org",
    ),
]
EXTENT = Extent(
    SpatialExtent([[-180.0, -60.0, 180.0, 82.75]]),
    TemporalExtent(
        [
            [
                str_to_datetime("2020-01-01T00:00:00Z"),
                str_to_datetime("2021-12-31T23:59:59Z"),
            ]
        ]
    ),
)
SUMMARIES = Summaries(
    {
        "platform": PLATFORM.split(", "),
        "instruments": INSTRUMENTS,
        "mission": MISSION.split(", "),
        "esa_worldcover:product_version": ["1.0.0", "2.0.0"],
    }
)
ITEM_ASSETS = {
    "map": AssetDefinition(
        {
            "type": MediaType.COG,
            "title": ASSET_PROPS["map"]["title"],
            "description": ASSET_PROPS["map"]["description"],
            "raster:bands": ASSET_PROPS["map"]["bands"],
            "classification:classes": ASSET_PROPS["map"]["classes"],
            "roles": ASSET_PROPS["map"]["roles"],
        }
    ),
    "input_quality": AssetDefinition(
        {
            "type": MediaType.COG,
            "title": ASSET_PROPS["inputquality"]["title"],
            "description": ASSET_PROPS["inputquality"]["description"],
            "raster:bands": ASSET_PROPS["inputquality"]["bands"],
            "roles": ASSET_PROPS["inputquality"]["roles"],
        }
    ),
}
USER_MANUAL_2020_LINK = Link(
    rel="about",
    target="https://esa-worldcover.s3.amazonaws.com/v100/2020/docs/WorldCover_PUM_V1.0.pdf",  # noqa
    media_type=MediaType.PDF,
    title="2020 Product Version 1.0.0 User Manual",
)
USER_MANUAL_2021_LINK = Link(
    rel="about",
    target="https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/docs/WorldCover_PUM_V2.0.pdf",  # noqa
    media_type=MediaType.PDF,
    title="2021 Product Version 2.0.0 User Manual",
)
VALIDATION_2020_LINK = Link(
    rel="about",
    target="https://worldcover2020.esa.int/data/docs/WorldCover_PVR_V1.1.pdf",
    media_type=MediaType.PDF,
    title="2020 Product Version 1.0.0 Validation Report",
)
VALIDATION_2021_LINK = Link(
    rel="about",
    target="https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/docs/WorldCover_PVR_V2.0.pdf",  # noqa
    media_type=MediaType.PDF,
    title="2021 Product Version 2.0.0 Validation Report",
)
