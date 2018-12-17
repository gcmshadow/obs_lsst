"""
LSST Cam-specific overrides for IsrTask
"""
if hasattr(config, 'ccdKeys'):
    config.ccdKeys = ['detector', 'snap', 'raftName', 'detectorName']

config.doLinearize = False
config.doDefect = False
config.doAddDistortionModel = False

# Work-around for median-bug in overscan correction (DM-15203).
config.overscanFitType = 'POLY'
config.overscanOrder = 0
