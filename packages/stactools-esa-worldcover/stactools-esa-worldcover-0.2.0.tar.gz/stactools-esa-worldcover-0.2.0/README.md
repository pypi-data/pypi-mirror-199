# stactools-esa-worldcover

[![PyPI](https://img.shields.io/pypi/v/stactools-esa-worldcover)](https://pypi.org/project/stactools-esa-worldcover/)

- Name: esa-worldcover
- Package: `stactools.esa-worldcover`
- [stactools-esa-worldcover on PyPI](https://pypi.org/project/stactools-esa-worldcover/)
- Owner: @pjhartzell
- [Dataset homepage](https://esa-worldcover.org/en)
- STAC extensions used:
  - [classification](https://github.com/stac-extensions/classification)
  - [item-assets](https://github.com/stac-extensions/item-assets)
  - [proj](https://github.com/stac-extensions/projection/)
  - [raster](https://github.com/stac-extensions/raster)
  - [scientific](https://github.com/stac-extensions/scientific)
- Extra fields:
  - `esa_worldcover:product_tile`: The lat/lon coordinates of the tile southwest corner
  - `esa_worldcover:product_version`: The version of the classification product

Generate STAC Items and Collections for the [ESA WorldCover](https://esa-worldcover.org/en) 10m resolution global land cover product based on Sentinel-1 and Sentinel-2 data.

## STAC Examples

- [Collection](examples/collection.json)
- [Item](examples/ESA_WorldCover_10m_2020_v100_N00E006/ESA_WorldCover_10m_2020_v100_N00E006.json)

## Installation

```shell
pip install stactools-esa-worldcover
```

## Command-line Usage

To create a STAC `Item`:

```shell
stac esa-worldcover create-item tests/data-files/ESA_WorldCover_10m_2020_v100_N00E006/ESA_WorldCover_10m_2020_v100_N00E006_Map.tif . --include-quality-asset
```

To create a STAC `Collection` from a text file containing a list of WorldCover Map tile COG files:

```shell
stac esa-worldcover create-collection tests/data-files/file-list.txt examples --include-quality-assets
```

The above `create-collection` command will create the contents of the `examples` directory.

Use `stac esa-worldcover --help` to see all subcommands and options.

## Contributing

We use [pre-commit](https://pre-commit.com/) to check any changes.
To set up your development environment:

```shell
pip install -e .
pip install -r requirements-dev.txt
pre-commit install
```

To check all files:

```shell
pre-commit run --all-files
```

To run the tests:

```shell
pytest -vv
```
