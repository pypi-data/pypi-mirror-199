import logging
from abc import ABC, abstractmethod
from typing import List, Set, Union
from os import PathLike
import os
from pathlib import Path

import numpy as np
from PIL import Image
import h5py as h5
import numpy as np

import config as cfg

logger = logging.getLogger(__name__)

class FileException(Exception):
    def __init__(self,
    message: str,
    path: PathLike):
        self.message = message
        self.path = path

    def __str__(self) -> str:
        return self.message

class FileHandler(ABC):
    @property
    @abstractmethod
    def valid_ext(self) -> Set:
        pass

    @property
    @abstractmethod
    def ext(self) -> str:
        '''Define the extension to use when saving files'''
        pass

    @abstractmethod
    def read(self, path: PathLike) -> np.ndarray:
        pass

    @abstractmethod
    def write(self, path: PathLike, data: np.ndarray, name: str=None) -> PathLike:
        ''' write the data to a file at the specified path. Specify the absolute path or path to a directory
        and a filename. In this case the default extension for the filetype will be used 
            Args:
                path: path to save the file to
                data: data to save
                name (optional): if the path provided is a directory, the filename can be specified here and the default
                    ext for that exporter will be applied
        '''
        pass

    def _check_path(self, path: PathLike) -> bool:
        '''checks the type of path and checks that the file extension is correct for import'''
        if not isinstance(path, PathLike):
            logger.warning(f"not pathlike, is instance of {type(path)}")
            return False
        if os.path.isfile(path) & (path.suffix in self.valid_ext):
            return True

        logger.warning(f"filetype should be one of {self.valid_ext}")
        return False

    def _get_complete_path(self, path: PathLike, name: str) -> PathLike:
        ''' constructs and validates the entire path to the file location for export'''
        if name is not None:
            ''' if no filename is specified then we will use the path provided '''
            path =  path / Path(name).with_suffix(self.ext)
        if not path.parent.absolute().exists():
            os.makedirs(path.parent.absolute(), exist_ok=True)
        return path

class LazyFile(ABC):
    ''' Facade for lazy loading of files. This class is used to wrap the file object and only load the data when it is'''
    def __init__(self, file: Union[h5.Dataset, Image.Image]) -> None:
        self.file = file

    def _check_slice_tuple(self, key: tuple, d: int, h: int, w: int) -> None:
        if not len(key) == 3 and all([isinstance(k, slice) for k in key]):
            raise ValueError(f"Invalid slice key: {key}")
        # make sure any undefined slices are set to the full range
        vol_shape = (d,w,h)
        for i, s in enumerate(key):
            if s.start is None:
                s.start = 0
            if s.stop is None:
                s.stop = vol_shape[i]
        return key
    
    @abstractmethod
    def __getitem__(self, key: Union[int, slice, tuple]) -> np.ndarray:
        pass
        
    @property
    @abstractmethod
    def shape(self) -> tuple:
        pass
    
    @property 
    @abstractmethod
    def chunking(self) -> tuple:
        pass
    
    @property
    @abstractmethod
    def total_chunks(self) -> int:
        pass
    
    @abstractmethod
    def __iter__(self) -> np.ndarray:
        ''' iterate over chunks/slices '''
        pass

class LazyH5(LazyFile):
    def __init__(self, file: h5.Dataset) -> None:
        super().__init__(file)
        logger.info(f"Total Volume Size: {self.file.shape}")
        self._d, self._h, self._w = self.file.shape

    def __getitem__(self, key: Union[int, slice, tuple]) -> np.ndarray:
        if isinstance(key, tuple):
            # a tuple should be a tuple of slices (D, H, W)
            key = self._check_slice_tuple(key, self._d, self._h, self._w)
            print(key)
            sd, sh, sw = key
            return np.array(self.file[sd, sh, sw])
        elif isinstance(key, slice):
            # a slice should be a slice of the z-axis
            return np.array(self.file[:, :, key])
        elif isinstance(key, int):
            # an int should be a slice of the z-axis
            return np.array(self.file[:, :, key])
        else:
            raise ValueError(f"Invalid key: {key}")
    
    def __iter__(self) -> np.ndarray:
        if isinstance(self.file, h5.Dataset):
            for chunk in self.file.iter_chunks():
                yield self.file[(chunk)]

    @property
    def shape(self) -> tuple:
        return self.file.shape

    @property
    def chunking(self) -> tuple:
        return self.file.chunks

    @property
    def total_chunks(self) -> int:
        return len(list(self.file.iter_chunks()))
   
class H5Handler(FileHandler):
    '''
    reads and writes hdf5 files
    '''
    def __init__(
        self,
        *,
        internal_path: str ="/data",
        chunking=True,
        compression="gzip",
        verbose: bool = False
    ):
        '''
        Args:
            internal_path (str): the internal path to the data in the hdf5 file
            chunking: the chunking to use
            compression: the compression to use
            verbose (bool): log additional information about the file
        '''
        self.internal_path = [i for i in internal_path.split('/') if i != '']
        self.chunking = chunking
        self.compression = compression
        self.verbose = verbose

    @property
    def valid_ext(self) -> Set:
        return cfg.HDF5_SUFFIXES

    @property
    def ext(self):
        return '.h5'

    def _get_target_dataset(self, paths: List[str], group: h5.Group):
        ''' Take all the remaining parts of the path and look at the next subgroup
        Args:
            paths (List[str]): the remaining parts of the path
            group (h5.Group): the current group to look in
        '''
        if paths[0] not in group.keys():
            raise FileException(f"Invalid Path for HDF5 read. {paths[0]} not found in {group}", group)
        
        item = group[paths[0]] # get the thing at the next level
        if self.verbose: logger.info(f"opening {paths[0]} in {group}")
        if isinstance(item, h5.Dataset):
            return item
        elif isinstance(item, h5.Group):
            return self._get_target_dataset(paths[1:], item)
        raise Exception(f"Invalid item type {type(item)}")

    def read(self, path: PathLike) -> LazyH5:
        """Returns a numpy array and chunking info when given a path
        to an HDF5 file.
        The data is assumed to be found in '/data' in the file.
        Args:
            path(pathlib.Path): The path to the HDF5 file.
            hdf5_path (str): The internal HDF5 path to the data.
        Returns:
            tuple(numpy.array, tuple(int, int)) : A numpy array
            for the data and a tuple with the chunking size.
        """

        if not self._check_path(path):
            raise FileException("Invalid Path for HDF5 read.", path)
        
        data_handle = h5.File(path, "r")

        if self.verbose:
            logger.info(f"Reading data from {path} with internal path {self.internal_path}")

        dataset = self._get_target_dataset(self.internal_path, data_handle)
        return LazyH5(dataset)

    def write(self, path: PathLike, data: np.ndarray, name: str=None) -> PathLike:
        '''
        Writes numpy array to hdf5 file. Takes an absolute path including filename
        or a path to a directory and a filename to use
        '''
        path = self._get_complete_path(path, name)
        logger.info(f"Saving data of shape {data.shape} to {path}")
        with h5.File(path, "w") as f:
            f.create_dataset(
                '/'+'/'.join(self.internal_path), data=data, chunks=self.chunking
            )
        return path
 
class LazyTiff(LazyFile):
    '''
    Facade for lazy loading single tiffs or multipage tiff files.
    '''
    def __init__(self, file: Image.Image) -> None:
        self.file = file
        self._h, self._w = np.shape(self.file)
        self._d = self.file.n_frames

    def __getitem__(self, key: Union[int, slice, tuple]) -> np.ndarray:
        if isinstance(key, int):
            try:
                self.file.seek(key)
                return np.array(self.file)
            except EOFError:
                raise IndexError(f"Index {key} out of range")
        elif isinstance(key, tuple):
            # a tuple should be a tuple of slices (D, H, W)
            key = self._check_slice_tuple(key, self._d, self._h, self._w)
            sd, sh, sw = key
            slices = []
            for s in range(*sd.indices(self._d)):
                try:
                    self.file.seek(s)
                except EOFError:
                    raise IndexError(f"Index {s} out of range")
                slices.append(np.array(self.file)[sh, sw])
            #return the array as (H, W, D)
            return np.array(slices).swapaxes(0, 2)
        elif isinstance(key, slice):
            # assume we are slicing over the first dimension (D)
            if key.start is None:
                key.start = 0
            if key.stop is None:
                key.stop = self._h
            slices = []
            for s in range(*key.indices(self._d)):
                try:
                    self.file.seek(s)
                except EOFError:
                    raise IndexError(f"Index {s} out of range")
                slices.append(np.array(self.file))
            return np.array(slices)
        
        raise ValueError(f"Invalid key: {key}")
            
    def __iter__(self):
        for i in range(self._d):
            self.file.seek(i)
            yield np.array(self.file)

    def __len__(self):
        return self._d

    @property
    def shape(self) -> tuple:
        return (self._h, self._w, self._d)

    @property
    def chunking(self) -> tuple:
        return (self._h, self._w, 1)

    @property
    def total_chunks(self) -> int:
        return self.file.n_frames
         
class TiffHandler(FileHandler):
    def __init__(self):
        pass

    @property
    def valid_ext(self) -> Set:
        return cfg.TIFF_SUFFIXES

    @property
    def ext(self):
        return '.tiff'

    def read(self, path: PathLike) -> LazyTiff:
        return LazyTiff(Image.open(path))

    def write(self, path: PathLike, data: np.ndarray, name: str=None) -> PathLike:
        pass
 
class LazyTiffStack(LazyFile):
    ''' Facade for lazy loading a stack of tiff files'''
    def __init__(self, files: List[Path], reader: FileHandler = TiffHandler()) -> None:
        self.files = files
        self._d = len(files)
        self._h, self._w, _ = np.shape(reader.read(files[0]))
        self.reader = reader
    
    def _get_frame(self, file: Path) -> np.ndarray:
        return np.ndarray(self.reader.read(file))
    
    def __getitem__(self, key: Union[int, slice, tuple]) -> np.ndarray:
        if isinstance(key, int):
            return self._get_frame(self.files[key])
        elif isinstance(key, tuple):
            key = self._check_slice_tuple(key, self._d, self._h, self._w)
            sd, sh, sw = key
            slices = []
            for s in range(*sd.indices(self._d)):
                slices.append(self._get_frame(self.files[s])[sh, sw])
            #return the array as (D, H, W)
            return np.array(slices)
        elif isinstance(key, slice):
            # assume we are slicing over the first dimension (D)
            if key.start is None:
                key.start = 0
            if key.stop is None:
                key.stop = self._h
            slices = []
            for s in range(*key.indices(self._d)):
                slices.append(self._get_frame(self.files[s]))
            return np.array(slices)
        
    def __iter__(self) -> np.ndarray:
        for i in range(self._d):
            yield self._get_frame(self.files[i])

    def __len__(self) -> int:
        return self._d
    
    def shape(self) -> tuple:
        return (self._h, self._w, self._d)
    
    def chunking(self) -> tuple:
        return (1, self._h, self._w)
    
    def total_chunks(self) -> int:
        return self._d

