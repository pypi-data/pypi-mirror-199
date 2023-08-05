from ast import Mult
from matplotlib.colors import from_levels_and_colors
from lenskappa.output.output import MultiCsvOutputHandler
from lenskappa.output.parser import weightsOutputParser
from pathlib import Path
import numpy as np
from astropy.coordinates import SkyCoord

cwd = Path.cwd()
combos = ["24_45", "24_120", "23_45", "23_120"]
paths = {c: cwd / ".".join([c, "csv"]) for c in combos}
columns = ["ra", "dec", "gal", "zweight", "oneoverr"]
rng = np.random.default_rng()
center = SkyCoord(1, 1, unit="deg")
test_weights = {}
for co in combos:
    control_weights = {}
    field_weights = {}
    for c in columns:
        control_values = rng.uniform(0.5, 2.0, 100)
        field_values = rng.uniform(0.5, 2.0, 100)
        control_weights.update({c: control_values})
        field_weights.update({c: field_values})
    test_weights.update({co: {"field_weights": field_weights, "control_weights": control_weights, "center": center}})

parser = MultiCsvOutputHandler(paths, weightsOutputParser, columns)
parser.take_output(test_weights)
parser.write_output()