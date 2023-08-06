from typing import Tuple, Union
import logging
import sys
from pathlib import Path
import crop_clip.resources.cc_types as cc_types
import crop_clip.resources.files as files
import crop_clip.config as cfg
import crop_clip.resources.utils as utils

logger = logging.getLogger(__name__)

def get_reader(path: Path, *, internal_path: str) -> files.FileHandler:
    ''' get the reader for single-file filetypes '''
    filetype = path.suffix
    if filetype in cfg.HDF5_SUFFIXES:
        if internal_path is None:
            logger.error(f"Internal path not specified. Using {cfg.DEFAULT_INTERNAL_PATH}.")
            internal_path = cfg.DEFAULT_INTERNAL_PATH
        # reading a hdf5 file
        return files.H5Handler(internal_path=internal_path)
    elif filetype in cfg.TIFF_SUFFIXES:
        return files.TiffHandler()
    else:
        print(type(filetype))
        logger.error(f"Filetype {filetype} not supported. Exiting!")
        sys.exit(1)

def crop(
    path: Path,
    output_path: Path,
    *,
    coords: cc_types.Crop = None,
    internal_path: str = None,
    offset: cc_types.Point3D = None,
    cube_size: Union[Tuple[int], int] = None,
):
    ''' 
    crop a subregion from volumetric data, supports specifying the region via 2 methods:
    1. specifying the coordinates of the top-left corner and the size of the cube
    2. specifying the coordinates of the top-left corner and the coordinates of the bottom-right corner

    internal_path must be specified for hdf5 files
    '''
    if coords is None and (offset is None or cube_size is None):
        raise ValueError("Must specify either coords or offset and cube_size")
    if coords is None:
        coords = resources.size_offset(cube_size, offset)

    logger.info(f"cropping to {coords}")
    if path.is_dir():
        logger.info(f"Assuming folder contains a tiff stack.")
        reader = files.TiffHandler()
        data = files.LazyTiffStack([f for f in path.iterdir() if f.suffix in cfg.TIFF_SUFFIXES])
        logger.info(f"found {len(data)} frames.")
    else:
        reader = get_reader(path, internal_path=internal_path)
        data: files.LazyFile = reader.read(path)

    resources.check_coords(coords, data.shape)
    region = data[coords.z0:coords.z1, coords.y0:coords.y1, coords.x0:coords.x1]
    writer = files.H5Handler(internal_path='data')

    out = writer.write(output_path, region, f"{path.stem}_crop")
    logger.info(f"cropped to {out}")