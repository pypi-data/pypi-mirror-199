from heinlein import load_dataset, Region

from lenskappa.catalog import SingleValueParam, MaxValueFilter, MinValueFilter
from astropy.coordinates import SkyCoord
import astropy.units as u
from shapely import geometry
from lenskappa.counting import RatioCounter

z_s_param = SingleValueParam('z_s', 2.375)
column_aliases = {"DNF_Z": "z_gal", "MAG_AUTO_I": "i_mag"}
center = SkyCoord(62.0906, -53.8999, unit="deg")

radius = 45*u.arcsec

lens_region = Region.circle(center, radius)

comparison_dataset = load_dataset("des")
comparison_dataset.add_aliases("catalog", column_aliases)

box = geometry.box(30, -35, 40, -30)
comparison_region = Region.polygon(box)


zmax_filter = MaxValueFilter('z_gal', 2.375)
magmax_filter = MaxValueFilter('i_mag', 24)
mindist_filter = MinValueFilter('r', min=6*u.arcsec)


field_data_45 = comparison_dataset.cone_search(center, radius, dtypes=["catalog", "mask"])
field_cat_45 = field_data_45["catalog"]
field_mask_45 = field_data_45["mask"]


counter = RatioCounter(field_data_45, comparison_dataset, lens_region, comparison_region, mask=True)
counter.add_catalog_filter(zmax_filter, name='zmax', filter_type='periodic', catalogs='all')
counter.add_catalog_filter(magmax_filter, name='magmax', filter_type='periodic', catalogs='all')
counter.add_catalog_filter(mindist_filter, name='mindist', filter_type='periodic', catalogs='all')
counter.add_weight_params({'z_s': 2.375})

counter.get_weights(['gal', 'zweight', 'oneoverr', 'zoverr'], output_file="/Users/patrick/code/Production/environment_study/lenskappa/lenskappa/tests/test_24_45.csv", num_samples=1000, threads=5, overwrite=True, meds=True)
