from lenskappa.counting import SingleCounter
from lenskappa.catalog import MaxValueFilter, MinValueFilter
import multiprocessing as mp
from heinlein import load_dataset

import astropy.units as u
from itertools import product
import functools
import pathlib


r_ = list(range(0,8))
allowed_fields = list(product(r_, r_))

def compute_counts(field, z_s, aperture, mag_i, output_dir):
    ms = load_dataset("ms")
    if field not in allowed_fields:
        print(f"Error: Field selected was {field}")
        return
    ms.set_field(field)
    zmax_filter = MaxValueFilter("z_gal", z_s)
    magmax_filter = MaxValueFilter("mag_i", mag_i)
    mindist_filter = MinValueFilter("r", 5*u.arcsec)
    ms.add_aliases("catalog", {"M_Stellar[M_sol/h]": "m_gal", 'mag_SDSS_i': 'mag_i', "z_spec": "z_gal"})
    ct = SingleCounter(ms, False)
    output_file = "ms_{}_{}_sampled.csv".format(field[0], field[1])
    output_path = pathlib.Path(output_dir) / output_file
    ct.add_weight_params({"z_s": z_s})
    ct.add_catalog_filter(zmax_filter, 'zmax')
    ct.add_catalog_filter(magmax_filter, 'magmax')
    ct.add_catalog_filter(mindist_filter, 'mindist')
    ct.get_weights(weights='all', meds=True, output_file = output_path, overlap=1, aperture=aperture)


if __name__ == "__main__":
    zs = 2.81
    aperture = 120*u.arcsec
    mag_i = 24
    output = "/Users/patrick/code/Production/environment_study/lenskappa/lenskappa/tests/0029"
    f = functools.partial(compute_counts, z_s = zs, aperture=aperture, mag_i = mag_i, output_dir = output)
    with mp.Pool(4) as p:
        p.map(f, allowed_fields)


    