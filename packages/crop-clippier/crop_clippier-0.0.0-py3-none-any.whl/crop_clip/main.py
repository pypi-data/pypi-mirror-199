import logging
from typing import Tuple
import sys
from pathlib import Path

import h5py as h5

import args as arguments
import config as cfg
import files
import cc_types
import utils

def size_offset(subregion_size: Tuple[int], subregion_offset: cc_types.Point3D) -> cc_types.Crop:
    return cc_types.Crop(
        x0=subregion_offset.x,
        x1=subregion_offset.x + subregion_size[0],
        y0=subregion_offset.y,
        y1=subregion_offset.y + subregion_size[1],
        z0=subregion_offset.z,
        z1=subregion_offset.z + subregion_size[2]
    )

def main():
    logging.basicConfig(
    level=logging.INFO, format=cfg.LOGGING_FMT,
    datefmt=cfg.LOGGING_DATE_FMT)
    logger = logging.getLogger(__name__)
    root_path = Path.cwd()
    parser = arguments.init_argparse()
    args: dict = vars(parser.parse_args())

    dims: bool = args["dims"]
    input_path: Path = Path(args['input_file_path'])
    cube_size: list = args["size"]
    if cube_size:
        cube_size = cube_size[0]
    coords: cc_types.Crop = args["coords"]
    offset:cc_types.Point3D = args["offset"]
    clip: bool = args["clip"]
    downsample: bool = args["downsample"]
    internal_path: str = args["internalpath"]
    if internal_path is not None:
        internal_path = internal_path[0]
    else:
        internal_path = cfg.DEFAULT_INTERNAL_PATH
    
    
    if input_path.is_dir():
        logger.info(f"Assuming folder contains a tiff stack.")
        reader = files.TiffHandler()
        data = files.LazyTiffStack([f for f in input_path.iterdir() if f.suffix in cfg.TIFF_SUFFIXES])
        logger.info(f"found {len(data)} frames.")
    else:
        filetype = input_path.suffix
        if filetype in cfg.HDF5_SUFFIXES:
            if internal_path is None: logger.error(f"Internal path not specified. Using {cfg.DEFAULT_INTERNAL_PATH}.")
            # reading a hdf5 file
            reader = files.H5Handler(internal_path=internal_path)
        elif filetype in cfg.TIFF_SUFFIXES:
            reader = files.TiffHandler()
        else:
            print(type(filetype))
            logger.error(f"Filetype {filetype} not supported. Exiting!")
            sys.exit(1)
        data: files.LazyFile = reader.read(input_path)

    if dims:
        logger.info(f"Dimensions of {input_path}: {data.shape}, (D, H, W)")
        sys.exit(0)

    if (cube_size and offset):
        logger.info("Using cube size and offset to define subvolume.")
        coords = size_offset((cube_size, cube_size, cube_size), offset)
    elif coords:
        logger.info("Using coords to define subvolume.")
    else:
        logger.info("Invalid combination of arguments. Exiting!")
        sys.exit(1)


    utils.check_coords(coords, data.shape)
    # pass in slices in order D, H, W
    # extract the subvolume from the lazy file
    logger.info(f"Selected Region: [{coords.z0}:{coords.z1}, {coords.y0}:{coords.y1}, {coords.x0}:{coords.x1}] (D, H, W)")
    region = data[coords.z0:coords.z1, coords.y0:coords.y1, coords.x0:coords.x1]
    writer = files.H5Handler(internal_path='data')
    if clip:
        region = utils.clip_to_uint8(data, reader, region, writer = writer)
    
    if downsample:
        logger.info(f"Downsampling not implemented yet.")

    output_path = root_path / f"{input_path.stem}_crop.h5"
    writer.write(output_path, region)
    logger.info(f"Saved cropped volume to {output_path}.")

if __name__ == "__main__":
    main()