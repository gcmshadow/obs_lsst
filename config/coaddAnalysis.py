"""
LSST Cam-specific overrides for CoaddAnalysisTask
"""
import os.path

from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask

# Reference catalog
config.refObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.refObjLoader.load(os.path.join(os.path.dirname(__file__), "filterMap.py"))
config.refObjLoader.ref_dataset_name="cal_ref_cat"

config.doWriteParquetTables=False
config.doApplyColorTerms=False
