import argparse
from typing import List, Union
import os

import h5py as h5

import crop_clip.config as cfg
import crop_clip.resources.cc_types as cc_types

# LOGGING FORMATTING
LOGGING_FMT = "%(asctime)s - %(levelname)s - %(message)s"
LOGGING_DATE_FMT = "%d-%b-%y %H:%M:%S"

def CheckExt(choices):
    """Wrapper to return the class
    """
    class Act(argparse.Action):
        """Class to allow checking of filename extensions in argparse. Taken
        from https://stackoverflow.com/questions/15203829/python-argparse-file-extension-checking
        """
        def __call__(self, parser, namespace, fname, option_string=None):
            ext = os.path.splitext(fname)[1][1:]
            if ext not in choices:
                option_string = f'({option_string})' if option_string else ''
                parser.error(f"Filetype {ext} is not valid: file doesn't end with {choices};{option_string}")
            else:
                setattr(namespace, self.dest, fname)

    return Act

class CreateCoords(argparse.Action):
    def __call__(
            self,
            parser: argparse.ArgumentParser,
            namespace: argparse.Namespace,
            values: List[int],
            option_string: Union[str, None] = None
        ) -> None:
        setattr(namespace, self.dest, cc_types.Crop(
            x0=values[4],
            x1=values[5],
            y0=values[2],
            y1=values[3],
            z0=values[0],
            z1=values[1]
        ))

class CreatePoint3D(argparse.Action):
    def __call__(
            self,
            parser: argparse.ArgumentParser,
            namespace: argparse.Namespace,
            values: List[int],
            option_string: Union[str, None] = None
        ) -> None:
        setattr(namespace, self.dest, cc_types.Point3D(
            x=values[0],
            y=values[1],
            z=values[2]
        ))

class InternalPath(argparse.Action):
    ''' the desired behaviour is that if this '''
    def __call__(
            self,
            parser: argparse.ArgumentParser,
            namespace: argparse.Namespace,
            values: str,
            option_string: Union[str, None] = None
        ) -> None:
        if values is None:
            print("parser was called")
            setattr(namespace, self.dest, cfg.DEFAULT_INTERNAL_PATH)
        else:
            setattr(namespace, self.dest, values)

def init_argparse() -> argparse.ArgumentParser:
    """Custom argument parser for this program.

    Returns:
        argparse.ArgumentParser: An argument parser with the appropriate
        command line args contained within.
    """
    parser = argparse.ArgumentParser(
        usage="%(prog)s [path/to/3d/image/data/file] options...",
        description="Cuts out and saves a smaller 3d volume from a larger 3d"\
        " imaging volume. Data can be downsampled and/or intensities clipped"\
        " followed by changing bit depth to uint8.\n\n"\
        " 2 modes are avaiable:\n"\
        " 1. Offset Mode: Specify the size of the cube and the offset from the top left of the volume\n"\
        " 2. Manual Mode: specify the coordinates of the top left and bottom right corners of the cube"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version 1.0.0"
    )
    parser.add_argument("input_file_path", metavar='Input file path', type=str,
                        action=CheckExt(cfg.INPUT_FILE_EXT),
                        help='the path to a file containing 3d image data.')
    parser.add_argument("--dims", action="store_true", help="print the dimensions of the input file and exit."),
    parser.add_argument('-i', '--internalpath', metavar='Internal file path for hdf5 files.',
                        nargs=1, type=str, action=InternalPath,)
    parser.add_argument('-s', '--size', nargs=1, type=int,
                        help='the size of the cube (default is 256).')
    parser.add_argument('--offset', nargs=3, type=int,
                        help='three values specifying the Z Y and X offset from the centre.',
                        action=CreatePoint3D)
    parser.add_argument('-d', '--downsample', nargs=1, type=int,
                        help='a factor to downsample the data by.')
    parser.add_argument('-c', '--clip',
                        action='store_true',
                        help="if specified the image intensities will be clipped, "
                        "rescaled and reduced to uint8 bit depth.")
    parser.add_argument('--coords',nargs=6, type=int,
                        help="specify coordinates for cube in the form: y_start, y_end,"
                        " x_start, x_end, z_start, z_end. (x,y,z = height, width, depth) Cannot be specfied in conjunction with"
                        " --size and/or--offset",
                        action=CreateCoords)
    return parser