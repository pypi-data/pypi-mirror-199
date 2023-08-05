import os.path
from tempfile import TemporaryDirectory
from typing import Callable, List

import pystac
from click import Command, Group
from stactools.testing.cli_test import CliTestCase

from stactools.esa_worldcover.commands import create_esaworldcover_command
from tests import test_data


class ItemCommandTest(CliTestCase):
    def create_subcommand_functions(self) -> List[Callable[[Group], Command]]:
        return [create_esaworldcover_command]

    def test_create_item(self) -> None:
        infile = test_data.get_path(
            "data-files/ESA_WorldCover_10m_2020_v100_N00E006/ESA_WorldCover_10m_2020_v100_N00E006_Map.tif"  # noqa
        )
        with TemporaryDirectory() as tmp_dir:
            cmd = f"esa-worldcover create-item {infile} {tmp_dir}"
            self.run_command(cmd)
            item_path = os.path.join(
                tmp_dir, "ESA_WorldCover_10m_2020_v100_N00E006.json"
            )
            item = pystac.read_file(item_path)
        item.validate()

    def test_create_collection(self) -> None:
        infile = test_data.get_path("data-files/file-list.txt")
        with TemporaryDirectory() as tmp_dir:
            cmd = f"esa-worldcover create-collection {infile} {tmp_dir} -q"
            self.run_command(cmd)
            collection_path = os.path.join(tmp_dir, "collection.json")
            collection = pystac.read_file(collection_path)
            collection.validate()
