import os
from datetime import datetime
from typing import Any, Dict, Optional

import numpy as np
import numpy.typing as npt
import rasterio
from pystac import Asset, MediaType
from pystac.extensions.projection import AssetProjectionExtension
from pystac.utils import make_absolute_href, str_to_datetime
from shapely.geometry import box, mapping, shape
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon
from stactools.core.io import ReadHrefModifier
from stactools.core.utils.raster_footprint import RasterFootprint

from stactools.esa_worldcover.constants import ASSET_PROPS


class Metadata:
    def __init__(
        self, href: str, read_href_modifier: Optional[ReadHrefModifier] = None
    ):
        if read_href_modifier:
            modified_href = read_href_modifier(href)
        else:
            modified_href = href
        with rasterio.open(modified_href) as dataset:
            self.bbox = list(dataset.bounds)
            self.transform = list(dataset.transform)[0:6]
            self.shape = dataset.shape
            self.tags = dataset.tags()

        self.href = href
        self.asset_type()

    def asset_type(self) -> None:
        filename = os.path.basename(self.href)
        self.root, _ = os.path.splitext(filename)
        self.type = self.root.split("_")[-1].lower()

    @property
    def item_id(self) -> str:
        return "_".join(self.root.split("_")[:-1])

    @property
    def geometry(self) -> Dict[str, Any]:
        geometry_dict: Dict[str, Any] = mapping(box(*self.bbox))
        return geometry_dict

    @property
    def tile(self) -> str:
        return str(self.tags["product_tile"])

    @property
    def version(self) -> str:
        return str(self.tags["product_version"][1:])

    @property
    def start_datetime(self) -> datetime:
        return str_to_datetime(self.tags["time_start"])

    @property
    def end_datetime(self) -> datetime:
        return str_to_datetime(self.tags["time_end"])

    @property
    def asset(self) -> Asset:
        asset = Asset(href=make_absolute_href(self.href))
        asset.roles = ASSET_PROPS[self.type]["roles"]
        asset.title = ASSET_PROPS[self.type]["title"]
        asset.description = ASSET_PROPS[self.type]["description"]
        asset.media_type = MediaType.COG

        extra_fields = {"raster:bands": ASSET_PROPS[self.type]["bands"]}
        if self.type == "map":
            extra_fields["classification:classes"] = ASSET_PROPS[self.type]["classes"]
        asset.extra_fields = extra_fields

        proj = AssetProjectionExtension.ext(asset)
        proj.transform = self.transform
        proj.shape = self.shape

        asset.common_metadata.created = str_to_datetime(self.tags["creation_time"])

        return asset

    @staticmethod
    def quality_href(map_href: str) -> str:
        base_href = "_".join(map_href.split("_")[:-1])
        return f"{base_href}_InputQuality.tif"


class ESAWorldCoverFootprint(RasterFootprint):
    """ESA WorldCover tiles are large (36000x36000 pixels), causing the numpy-
    based mask computation to consume >30GB for some tiles. This is more than
    many machines support. This subclass avoids mask computation by assuming
    the data array used to initialize the class is a rasterio mask.
    """

    def data_mask(self) -> npt.NDArray[np.uint8]:
        # We will use a rasterio mask as the data array in the initializer, so
        # no mask computation is required
        return self.data_array

    def data_extent(self, mask: npt.NDArray[np.uint8]) -> Optional[Polygon]:
        data_polygons = [
            shape(polygon_dict)
            for polygon_dict, region_value in rasterio.features.shapes(
                mask, transform=self.transform
            )
            if region_value == 255  # rasterio masks use 255 for True (not 1)
        ]

        if not data_polygons:
            return None
        elif len(data_polygons) == 1:
            polygon = data_polygons[0]
        else:
            polygon = MultiPolygon(data_polygons).convex_hull

        return polygon
