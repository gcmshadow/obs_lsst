# This file is part of obs_lsst.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import os
import sys
import unittest
import unittest.mock

import lsst.utils.tests
from lsst.geom import arcseconds, Extent2I
import lsst.afw.image

from lsst.obs.lsst.testHelper import ObsLsstButlerTests, ObsLsstObsBaseOverrides
TESTDIR = os.path.abspath(os.path.dirname(__file__))


class TestPhosim(ObsLsstObsBaseOverrides, ObsLsstButlerTests):
    instrumentDir = "phosim"

    def setUp(self):
        dataIds = {'raw': {'expId': 204595, 'detectorName': 'S20', 'raftName': 'R11'},
                   'bias': unittest.SkipTest,
                   'flat': unittest.SkipTest,
                   'dark': unittest.SkipTest
                   }
        self.setUp_tests(self._butler, self._mapper, dataIds)

        ccdExposureId_bits = 38
        exposureIds = {'raw': 204595042}
        filters = {'raw': 'i'}
        exptimes = {'raw': 30.0}
        detectorIds = {'raw': 42}
        detector_names = {'raw': 'R11_S20'}
        detector_serials = {'raw': 'ITL-3800C-102-Dev'}
        dimensions = {'raw': Extent2I(4176, 4020)}
        sky_origin = (55.67759886, -30.44239357)
        raw_subsets = (({'level': 'sensor'}, 1),
                       ({'level': 'sensor', 'filter': 'i'}, 1),
                       ({'level': 'sensor', 'filter': 'foo'}, 0),
                       ({'level': 'sensor', 'visit': 204595}, 1),
                       ({'level': 'filter'}, 1),
                       ({'level': 'filter', 'visit': 204595}, 1),
                       ({'level': 'expId'}, 1),
                       ({'level': 'expId', 'filter': 'i'}, 1),
                       ({'level': 'expId', 'filter': 'foo'}, 0)
                       )
        linearizer_type = unittest.SkipTest
        self.setUp_butler_get(ccdExposureId_bits=ccdExposureId_bits,
                              exposureIds=exposureIds,
                              filters=filters,
                              exptimes=exptimes,
                              detectorIds=detectorIds,
                              detector_names=detector_names,
                              detector_serials=detector_serials,
                              dimensions=dimensions,
                              sky_origin=sky_origin,
                              raw_subsets=raw_subsets,
                              linearizer_type=linearizer_type
                              )

        path_to_raw = os.path.join(self.data_dir, "raw", "204595", "R11", "00204595-R11-S20-det042.fits")
        keys = set(('filter', 'patch', 'tract', 'visit', 'channel', 'amp', 'style', 'detector', 'dstype',
                    'snap', 'run', 'calibDate', 'half', 'detectorName', 'raftName', 'label',
                    'numSubfilters', 'fgcmcycle', 'name', 'pixel_id', 'description', 'subfilter', 'expId',
                    'dayObs', 'seqNum', 'subdir',))
        query_format = ["expId", "filter"]
        queryMetadata = (({'expId': 204595}, [(204595, 'i')]),
                         ({'filter': 'i'}, [(204595, 'i')]),
                         )
        map_python_type = lsst.afw.image.DecoratedImageF
        map_python_std_type = lsst.afw.image.ExposureF
        map_cpp_type = 'DecoratedImageF'
        map_storage_name = 'FitsStorage'
        metadata_output_path = os.path.join('processCcd_metadata', '00204595-i', 'R11',
                                            'processCcdMetadata_00204595-i-R11-S20-det042.yaml')
        raw_filename = '00204595-R11-S20-det042.fits'
        default_level = 'sensor'
        raw_levels = (('sensor', set(['expId', 'detector', 'run', 'detectorName', 'raftName'])),
                      ('skyTile', set(['expId', 'run'])),
                      ('filter', set(['expId'])),
                      ('expId', set(['expId', 'run']))
                      )
        self.setUp_mapper(output=self.data_dir,
                          path_to_raw=path_to_raw,
                          keys=keys,
                          query_format=query_format,
                          queryMetadata=queryMetadata,
                          metadata_output_path=metadata_output_path,
                          map_python_type=map_python_type,
                          map_python_std_type=map_python_std_type,
                          map_cpp_type=map_cpp_type,
                          map_storage_name=map_storage_name,
                          raw_filename=raw_filename,
                          default_level=default_level,
                          raw_levels=raw_levels,
                          test_config_metadata=True
                          )

        self.setUp_camera(camera_name='LSSTCam-PhoSim',
                          n_detectors=201,
                          first_detector_name='R01_S00',
                          plate_scale=20.0 * arcseconds,
                          )

        super().setUp()

    def testMetadata(self):
        """Check that we can read headers properly"""
        dataId = {'expId': 204595, 'detectorName': 'S20', 'raftName': 'R11'}
        md = self.butler.get("raw_md", dataId)

        # This header comes from amp header
        self.assertEqual(md["PRESS"], 520.0)

        # This header is in HDU0
        self.assertEqual(md["TESTTYPE"], "PHOSIM")

        visitInfo = self.butler.get("raw_visitInfo", dataId)
        weather = visitInfo.getWeather()
        self.assertEqual(weather.getAirTemperature(), 20.0)

        # Check that corrections are being applied
        with unittest.mock.patch.dict(os.environ,
                                      {"METADATA_CORRECTIONS_PATH": os.path.join(TESTDIR, "data")}):
            # Check that corrections are applied during simple md get
            md_md = self.butler.get("raw_md", dataId)
            self.assertEqual(md_md["NEWHDR"], "corrected")

            # Check that corrections are applied if we do assembly
            raw = self.butler.get("raw", dataId)
            raw_md = raw.getMetadata()
            self.assertEqual(raw_md, md_md)

            # And finally ensure that visitInfo gets corrections
            visitInfo = self.butler.get("raw_visitInfo", dataId)
            weather = visitInfo.getWeather()
            self.assertEqual(weather.getAirTemperature(), 10.0)

    def testCcdExposureId(self):
        with self.assertRaises(KeyError):
            self.butler.get('ccdExposureId', dataId={})

        exposureId = self.butler.get('ccdExposureId', dataId={"visit": 1, "detector": 1})
        self.assertEqual(exposureId, 1001)

        exposureId = self.butler.get('ccdExposureId', dataId={"visit": 1, "raftName": "R01",
                                                              "detectorName": "S01"})
        self.assertEqual(exposureId, 1001)

        with self.assertRaises(ValueError):
            self.butler.get('ccdExposureId', dataId={"visit": 1, "detector": 2000})

        with self.assertRaises(KeyError):
            self.butler.get('ccdExposureId', dataId={"visit": 1})

        with self.assertRaises(ValueError):
            self.butler.get('ccdExposureId', dataId={"visit": 1, "raftName": "R99",
                                                     "detectorName": "S01"})

    def testDetectorName(self):
        name = self.mapper._extractDetectorName({"raftName": "R00", "detectorName": "S00"})
        self.assertEqual(name, "R00_S00")

        name = self.mapper._extractDetectorName({'visit': 204595, 'detectorName': 'S20'})
        self.assertEqual(name, "R11_S20")

        name = self.mapper._extractDetectorName({'visit': 204595, 'detector': 42})
        self.assertEqual(name, "R11_S20")

        name = self.mapper._extractDetectorName({'detector': 42})
        self.assertEqual(name, "R11_S20")

        name = self.mapper._extractDetectorName({'visit': 204595})
        self.assertEqual(name, "R11_S20")

        with self.assertRaises(RuntimeError):
            self.mapper._extractDetectorName({'visit': 1})


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == '__main__':
    setup_module(sys.modules[__name__])
    unittest.main()
