import pydantic
from pydantic import BaseModel, validator

class Crop(BaseModel):
    '''
    x0: x coordinate of the top left corner
    y0: y coordinate of the top left corner
    x1: x coordinate of the bottom right corner
    y1: y coordinate of the bottom right corner
    z0: index of first slice
    z1: index of last slice
    '''
    x0: int
    y0: int
    x1: int
    y1: int
    z0: int
    z1: int

    @validator('*', pre=True)
    def check_coords(cls, v):
        if v < 0:
            raise ValueError('coords should be a list of positive integers')
        return v

class Point3D(BaseModel):
    x: int
    y: int
    z: int

    @validator('*', pre=True)
    def check_coords(cls, v):
        if v < 0:
            raise ValueError('coords should be a list of positive integers')
        return v

class Point2D(BaseModel):
    x: int
    y: int

    @validator('*', pre=True)
    def check_coords(cls, v):
        if v < 0:
            raise ValueError('coords should be a list of positive integers')
        return v