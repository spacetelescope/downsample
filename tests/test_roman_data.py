from pathlib import Path

import pytest

from stpreview.downsample import downsample_asdf

DATA_DIRECTORY = Path(__file__).parent / "data"
if not DATA_DIRECTORY.exists():
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

SHARED_DATA_DIRECTORY = Path("/grp/roman/TEST_DATA/23Q4_B11/aligntest")


def level1_science_raw(data_directory) -> Path:
    filename = data_directory / "level1_science_raw.asdf"
    if not filename.exists():
        from roman_datamodels.maker_utils import mk_level1_science_raw

        mk_level1_science_raw(filepath=filename)

    return filename


def level2_image(data_directory) -> Path:
    filename = data_directory / "level2_image.asdf"
    if not filename.exists():
        from roman_datamodels.maker_utils import mk_level2_image

        mk_level2_image(filepath=filename)

    return filename


def level3_mosaic(data_directory) -> Path:
    filename = data_directory / "level3_mosaic.asdf"
    if not filename.exists():
        from roman_datamodels.maker_utils import mk_level3_mosaic

        mk_level3_mosaic(filepath=filename)

    return filename


@pytest.mark.parametrize(
    "filename,shape",
    [
        (level1_science_raw(DATA_DIRECTORY), 3),
        (level2_image(DATA_DIRECTORY), 2),
        (level3_mosaic(DATA_DIRECTORY), 2),
    ],
)
def test_dummy_data(filename, shape):
    result = downsample_asdf(filename, by=2)

    assert len(result.shape) == shape


@pytest.mark.shareddata
@pytest.mark.skipif(
    not SHARED_DATA_DIRECTORY.exists(), reason="can't reach shared data directory"
)
@pytest.mark.parametrize(
    "filename,shape",
    [
        (filename, 3 if "uncal" in str(filename) else 2)
        for filename in SHARED_DATA_DIRECTORY.iterdir()
        if filename.suffix.lower() == ".asdf"
    ]
    if SHARED_DATA_DIRECTORY.exists()
    else [],
)
def test_sample_data(filename, shape):
    result = downsample_asdf(filename, by=2)

    assert len(result.shape) == shape
