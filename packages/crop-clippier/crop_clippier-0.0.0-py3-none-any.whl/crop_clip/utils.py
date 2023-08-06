from typing import List, Tuple, Union
import logging
import sys
from tqdm import tqdm

import cc_types
import files
import config as cfg

# from crop_clip import cc_types
# from crop_clip import files
# from crop_clip import config as cfg

import numpy as np

logger = logging.getLogger(__name__)

def check_coords(coords: cc_types.Crop, data_shape: Tuple[int]) -> bool:
    """Checks that the coordinates are valid for the data shape.

    Args:
        coords (coords): The coordinates to check.
        data_shape (Tuple[int]): The shape of the data.

    Returns:
        bool: True if the coordinates are valid, False otherwise.
    """
    coords = [coords.z0, coords.z1, coords.y0, coords.y1, coords.x0, coords.x1]
    axes = [0,0,1,1,2,2]
    if any([coord > data_shape[axes[i]] for i, coord in enumerate(coords)]):
        logger.error(f'Coordinates {coords} are out of bounds of volume with shape (H: {data_shape[0]}, W: {data_shape[1]}, D: {data_shape[2]}).')
        sys.exit(1)
    return True

def clip_to_uint8(data: files.LazyFile, reader: files.FileHandler, region: np.ndarray, *, writer: files.FileHandler = None) -> np.ndarray:
    """Clip the data to the range [0, 255] and convert to uint8.

    Args:
        data (np.ndarray): The original data volume in a Lazy-loading wrapper.
        reader (files.FileHandler): The file handler for the data.
        region (np.ndarray): The region of the data to clip.
    
    Keyword Args:
        writer (files.FileHandler): The file handler for the output data.
        Defaults to using the same handler as the reader.

    Returns:
        np.ndarray: The clipped data.
    """
    if writer is None:
        writer = reader
    region_size = region.size

    total = 0.0
    standard_deviations = []
    for d in tqdm(data, desc="Calculating mean and standard deviation", total=data.total_chunks):
        total += np.sum(d)
        standard_deviations.append(np.std(d))
    mean = total / np.prod(data.shape)
    avg_std = np.mean(standard_deviations)

    lwr_bound = mean - (avg_std * cfg.STDEV_FACTOR)
    upr_bound = mean + (avg_std * cfg.STDEV_FACTOR)
    
    with np.errstate(invalid='ignore'):
            gt_ub = (region > upr_bound).sum()
            lt_lb = (region < lwr_bound).sum()
    logger.info(f"Lower bound: {lwr_bound}, upper bound: {upr_bound}")
    logger.info(
        f"Number of voxels above upper bound to be clipped {gt_ub} - percentage {gt_ub/region_size * 100:.3f}%")
    logger.info(
        f"Number of voxels below lower bound to be clipped {lt_lb} - percentage {lt_lb/region_size * 100:.3f}%")
    
    if np.isnan(region).any():
        logger.info(f"Replacing NaN values.")
        region = np.nan_to_num(region, copy=False, nan=mean)

    logger.info("Rescaling intensities.")
    if np.issubdtype(region.dtype, np.integer):
        logger.info("region is already in integer dtype, converting to float for rescaling.")
        region = region.astype(np.float32)
    
    region = np.clip(region, lwr_bound, upr_bound, out=region)
    region = np.subtract(region, lwr_bound, out=region)
    region = np.divide(region, (upr_bound - lwr_bound), out=region)
    region = np.clip(region, 0.0, 1.0, out=region)
    logger.info("Converting to uint8.")
    region = np.multiply(region, 255, out=region)
    return region.astype(np.uint8)