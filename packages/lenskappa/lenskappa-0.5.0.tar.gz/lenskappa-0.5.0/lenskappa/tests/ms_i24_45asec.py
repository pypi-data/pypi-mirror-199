from lenskappa.spatial import SkyRegion, CircularSkyRegion
from lenskappa.counting import SingleCounter
from lenskappa.catalog import SkyCatalog2D, MaxValueFilter, MinValueFilter, QuantCatalogParam
from lenskappa.catalog import sampling
from lenskappa.datasets.surveys import ms as millenium
import multiprocess

from astropy.coordinates import SkyCoord
import astropy.units as u
from shapely import geometry
import logging
import time
import os

def get_range(x_range, y_range, output_dir, sampling_pars):
    weights = 'all'
    zmax_filter = MaxValueFilter('z_gal', 1.523)
    magmax_filter = MaxValueFilter('mag_i', 24.0)
    mindist_filter = MinValueFilter('r', 5*u.arcsec)
    param = [QuantCatalogParam("M_Stellar[M_sol/h]", "m_gal"), QuantCatalogParam('mag_SDSS_i', 'mag_i')]
    dist_array = sampling.GaussianDistributionArray(relative=True, target='z_gal', positive=True)
    dist_array.add_distributions(['z_gal', 'mag_i'], *sampling_pars)

    aperture = 45*u.arcsec
    for i_x in x_range:
        for i_y in y_range:
            mils = millenium()
            ct = SingleCounter(mils, False)
            output_file = "ms_{}_{}_sampled.csv".format(i_x, i_y)
            output_path = os.path.join(output_dir, output_file)
            mils.load_catalogs_by_field(i_x,i_y,z_s = 1.523, params=param)
            mils.attach_dist_array(dist_array, 'z_gal')
            ct.add_catalog_filter(zmax_filter, 'zmax')
            ct.add_catalog_filter(magmax_filter, 'magmax')
            ct.add_catalog_filter(mindist_filter, 'mindist')
            ct.get_weights(output_positions=True, weights=weights, meds=True, output_file = output_path, overlap=4,aperture=aperture, n_samples=10)

if __name__ == "__main__":


    import pickle
    root = "/home/prwells/data/J0924"
    grid_path = root + "/grid.dat"
    std_path = root + "/std_means.dat"
    bias_path = root + "/bias_means.dat"

    with open(grid_path, "rb") as f:
        grid = pickle.load(f)
    with open(std_path, 'rb') as f:
        stds = pickle.load(f)
    with open(bias_path, 'rb') as f:
        biases = pickle.load(f)



    all = [[0],[1],[2],[3],[4], [5], [6], [7]]
    output_dir = "/home/prwells/outputs/j0924_weighting/final/ms/45asec_i24"
    processes = []
    for ix, x in enumerate(all):
        for iy, y in enumerate(all):
            if (ix == 0) and (iy == 0):
                continue
            p = multiprocess.Process(target = get_range, args=(x, y, output_dir, [grid, biases, stds]))
            p.start()
            processes.append(p)
    get_range([0], [0], output_dir)
    for p in processes:
        p.join()
