from lenskappa.counting import RatioCounter
from lenskappa.catalog import MaxValueFilter, MinValueFilter, QuantCatalogParam, SingleValueParam

import pandas as pd
from astropy.coordinates import SkyCoord
import astropy.units as u
from shapely import geometry
import logging
import time
from heinlein import Region
from heinlein import load_dataset

############
#Load the dataset
# hsc = load_dataset("hsc")
cfht = load_dataset("cfht")


############ think we may only need redshift and _____
#lenskappa expects standard column names, but individual surveys all use their own colum names
# column_aliases = {'demp_sm': 'm_gal', "demp_photoz_best": "z_gal"}
column_aliases = {'LP_log10_SM_MED': 'm_gal', "Z_B": "z_gal"} # m_gal seems to be stellar mass?
cfht.add_aliases("catalog", column_aliases)

#Tell lenskappa what region of the sky we'd like to look at (something around 50 square degrees-ish, must be inside the cfht survey)
# (must have 4-5 different fields named, dont have them yet)
box = geometry.box(30.25, -11.25, 38.75, -3.75) # min ra min dec, min dec to max dec ######## DOUBLE CHECK THIS ##########
comparison_region = Region.polygon(box)

# How big of an aperture we're looking at. # used to be 120 because that historically was the largest they could fit on a detector
# past 160, objects are too far to have an effect
radius = 45*u.arcsec


#Grab the data for the lens we're interested in # all of them should be in cfht and grabbable
# center = SkyCoord(24.520, 54.82, unit="deg")
center = SkyCoord('02 08 33.10', '-07 14 14.1', unit=(u.hourangle, u.deg))
lens_data = cfht.cone_search(center, radius,dtypes=["catalog", "mask"])
lens_region = Region.circle(center, radius)

#We remove some objects from the catalog.
zmax_filter = MaxValueFilter('z_gal', 3.48) #Remove objects farther away than the source
magmax_filter = MaxValueFilter('MAG_i', 23.0) #Remove objects that are too faint
mindist_filter = MinValueFilter('r', 5*u.arcsec) #Remove objects that are too close to the center of the field


#Create the counter, and give it the important information
counter = RatioCounter(lens_data, cfht, lens_region, comparison_region, mask=True)
counter.add_catalog_filter(zmax_filter, 'z_max')
counter.add_catalog_filter(magmax_filter, 'mag_max')
counter.add_catalog_filter(mindist_filter, 'mindist')
counter.add_weight_params({'z_s': 3.48}) #Some of the weights need the redshift of the source, so we give it that
#Note: Future versions will make it so we only have to give it the redshift of the source once


#Run the analysis
start_time = time.time()
output_path = "/Users/patrick/code/Production/environment_study/lenskappa/lenskappa/tests/cfht_test.csv"
#Note 'all' here means to get all the weights. You could replace it with a list of the ones you want if you don't want them all
# meds also computes it with the median
counter.get_weights(['gal', 'zweight', 'oneoverr', 'massoverr'], output_file=output_path, num_samples=200, threads=8, overwrite=True, meds=True)
end_time = time.time()
timediff = end_time - start_time
print("Completed in {} seconds".format(timediff))