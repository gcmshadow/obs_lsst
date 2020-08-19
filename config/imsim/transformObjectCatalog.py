import os
from lsst.utils import getPackageDir

config.filterMap = {band: band for band in 'ugrizy'}
config.functorFile = os.path.join(getPackageDir('obs_lsst'), 'policy', 'imsim', 'Object.yaml')
