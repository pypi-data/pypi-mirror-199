include("./kappa.jl")
using CSV

lower_bound = 0.1
upper_bound = 3.0
nbins = 100

kappa_bins = range(-0.2, 0.4, 1000)
dbin = (upper_bound - lower_bound) / nbins
weights = ["gal", "zweight"]

path = "/Users/patrick/Documents/Documents/Work/Research/Environment/des/DES0029/field/24_45.csv"
distribution = build_distribution(path, weights, nbins, lower_bound, upper_bound)

df = load_ms_weights("/Users/patrick/Documents/Documents/Work/Research/Environment/des/DES0029/ms/24_45")
selected_weights = df[:, weights]
selected_weights = normalize_ms_weights(selected_weights)
ms_partitions = partition_ms(selected_weights, lower_bound:dbin:upper_bound)
