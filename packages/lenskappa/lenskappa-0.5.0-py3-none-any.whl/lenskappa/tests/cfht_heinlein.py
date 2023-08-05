from heinlein import load_dataset, Region

from lenskappa.catalog import SingleValueParam, MaxValueFilter, MinValueFilter
from astropy.coordinates import SkyCoord
import astropy.units as u
from shapely import geometry
from lenskappa.counting import RatioCounter
from time import sleep


radius = 45*u.arcsec
cfht = load_dataset("cfht")
center = SkyCoord('02 08 33.10', '-07 14 14.1', unit=(u.hourangle, u.deg))
lens_data = cfht.cone_search(center, radius,dtypes=["catalog", "mask"])

sleep(10)