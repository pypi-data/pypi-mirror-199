import logging
import os

import click
from click import Command, Group
from pystac import CatalogType

from stactools.esa_worldcover import stac

logger = logging.getLogger(__name__)


def create_esaworldcover_command(cli: Group) -> Command:
    """Creates the stactools-esa-worldcover command line utility."""

    @cli.group(
        "esa-worldcover",
        short_help=("Commands for working with ESA WorldCover"),
    )
    def esaworldcover() -> None:
        pass

    @esaworldcover.command(
        "create-collection",
        short_help="Creates a STAC collection of ESA WorldCover product tiles.",
    )
    @click.argument("INFILE")
    @click.argument("OUTDIR")
    @click.option(
        "-i",
        "--id",
        default="esa-worldcover",
        show_default=True,
        help="collection id string",
    )
    @click.option(
        "-q",
        "--include-quality-assets",
        is_flag=True,
        help="include input quality raster Assets in Items",
    )
    @click.option(
        "-r",
        "--raster-footprint",
        default=False,
        show_default=True,
        help="use footprint of valid raster data for Item geometry",
    )
    def create_collection_command(
        infile: str,
        outdir: str,
        id: str,
        include_quality_assets: bool,
        raster_footprint: bool,
    ) -> None:
        """Creates a STAC Collection for Items defined by the hrefs in INFILE."

        \b
        Args:
            infile (str): Text file containing one href per line. The hrefs
                should point to ESA WorldCover 3x3 degree tile Map COGs.
            outdir (str): Directory that will contain the collection.
            id (str): Collection id. Defaults to "esa-worldcover".
            quality_assets (bool): Flag to include input quality Assets in the
                collection Items. Requires input quality COGs to exist alongside
                the corresponding map COG hrefs listed in INFILE.
            raster_footprint (bool): Flag to use the footprint of valid (not
                nodata) raster data for the Item geometry. Default is False.

        """
        with open(infile) as file:
            hrefs = [line.strip() for line in file.readlines()]

        collection = stac.create_collection(id)
        collection.set_self_href(os.path.join(outdir, "collection.json"))
        collection.catalog_type = CatalogType.SELF_CONTAINED
        for href in hrefs:
            item = stac.create_item(
                href,
                include_quality_asset=include_quality_assets,
                raster_footprint=raster_footprint,
            )
            collection.add_item(item)
        collection.make_all_asset_hrefs_relative()
        collection.validate_all()
        collection.save()

    @esaworldcover.command(
        "create-item",
        short_help=("Create a STAC Item from an ESA WorldCover Map COG file."),
    )
    @click.argument("INFILE")
    @click.argument("OUTDIR")
    @click.option(
        "-q",
        "--include-quality-asset",
        is_flag=True,
        help="include input quality raster Asset in Item",
    )
    @click.option(
        "-r",
        "--raster-footprint",
        default=False,
        show_default=True,
        help="use footprint of valid raster data for Item geometry",
    )
    def create_item_command(
        infile: str,
        outdir: str,
        include_quality_asset: bool,
        raster_footprint: bool,
    ) -> None:
        """Creates a STAC Item for a 3x3 degree tile of the ESA 10m WorldCover
        classification product.

        \b
        Args:
            infile (str): HREF of the classification map COG.
            outdir (str): Directory that will contain the STAC Item.
            quality_asset (bool): Flag to include an input quality asset.
                Requires an input quality COG to exist alongside the map COG.
            raster_footprint (bool): Flag to use the footprint of valid (not
                nodata) raster data for the Item geometry. Default is False.

        """
        item = stac.create_item(
            infile,
            include_quality_asset=include_quality_asset,
            raster_footprint=raster_footprint,
        )
        item_path = os.path.join(outdir, f"{item.id}.json")
        item.set_self_href(item_path)
        item.make_asset_hrefs_relative()
        item.validate()
        item.save_object()

    return esaworldcover
