from abc import ABC, abstractmethod
import logging
from heinlein import load_dataset
import astropy.units as u
from heinlein.dataset.dataset import Dataset
from heinlein.region import PolygonRegion, Region
from astropy.coordinates import SkyCoord

def get_region_picker(rtype, comparison_region, *args, **kwargs):
    if rtype != "circle":
        logging.critical("Error, only circular regions are currently supported")
        exit()
    return circularRegionRandomSampler(comparison_region=comparison_region, *args, **kwargs)


class regionPicker(ABC):

    def __init__(self, comparison_region: PolygonRegion, *args, **kwargs):
        self._comparison_region = comparison_region

    @abstractmethod
    def pick_region(self, *args, **kwargs):
        pass

    @abstractmethod
    def pick_many_regions(self, *args, **kwargs):
        pass

    @abstractmethod
    def coord_to_region(self, *args, **kwargs):
        pass

class circularRegionRandomSampler(regionPicker):
    def __init__(self, radius, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.radius = radius
        self.check_radius()

    def check_radius(self, *args, **kwargs):
        if type(self.radius) == list:
            self.radius.sort()
            self.query_radius = self.radius[-1]
        else:
            self.query_radius = self.radius


    def pick_region(self, *args, **kwargs):
        return self._comparison_region.generate_circular_tile(self.query_radius)
    
    def pick_many_regions(self, n, *args, **kwargs):
        return self._comparison_region.generate_circular_tiles(self.query_radius, n)

    def coord_to_region(self, coord: SkyCoord, *args, **kwargs):
        return Region.circle(coord, self.query_radius)