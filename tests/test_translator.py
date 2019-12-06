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

import os.path
import unittest
import astropy
import astropy.units as u
import astropy.units.cds as cds
import lsst.obs.lsst.translators  # noqa: F401 -- register the translators

from astro_metadata_translator.tests import MetadataAssertHelper

TESTDIR = os.path.abspath(os.path.dirname(__file__))


class LsstMetadataTranslatorTestCase(unittest.TestCase, MetadataAssertHelper):
    """Each test reads in raw headers from YAML files, constructs an
    `ObservationInfo`, and compares the properties with the expected values
    defined in the corresponding `dict`."""

    datadir = os.path.join(TESTDIR, "headers")

    def test_lsstCam_translator(self):
        test_data = (("lsstCam-MC_C_20190319_000001_R10_S02.yaml",
                      dict(telescope="LSST",
                           instrument="lsstCam",
                           boresight_rotation_coord="unknown",
                           dark_time=0.0*u.s,
                           detector_exposure_id=2019031900001029,
                           detector_group="R10",
                           detector_name="S02",
                           detector_num=29,
                           detector_serial="ITL-3800C-041",
                           exposure_id=2019031900001,
                           exposure_time=0.0*u.s,
                           object="UNKNOWN",
                           observation_id="MC_C_20190319_000001",
                           observation_type="bias",
                           physical_filter="NONE",
                           pressure=None,
                           relative_humidity=None,
                           science_program="unknown",
                           temperature=None,
                           visit_id=2019031900001)),
                     ("lsstCam-MC_C_20190319_000001_R22_S21.yaml",
                      dict(telescope="LSST",
                           instrument="lsstCam",
                           boresight_rotation_coord="unknown",
                           dark_time=0.0*u.s,
                           detector_exposure_id=2019031900001097,
                           detector_group="R22",
                           detector_name="S21",
                           detector_num=97,
                           detector_serial="ITL-3800C-139",
                           exposure_id=2019031900001,
                           exposure_time=0.0*u.s,
                           object="UNKNOWN",
                           observation_id="MC_C_20190319_000001",
                           observation_type="bias",
                           physical_filter="NONE",
                           pressure=None,
                           relative_humidity=None,
                           science_program="unknown",
                           temperature=None,
                           visit_id=2019031900001)),
                     ("lsstCam-MC_C_20190322_000002_R10_S22.yaml",
                      dict(telescope="LSST",
                           instrument="lsstCam",
                           boresight_rotation_coord="unknown",
                           dark_time=1.0*u.s,
                           detector_exposure_id=2019032200002035,
                           detector_group="R10",
                           detector_name="S22",
                           detector_num=35,
                           detector_serial="ITL-3800C-103",
                           exposure_id=2019032200002,
                           exposure_time=1.0*u.s,
                           object="UNKNOWN",
                           observation_id="MC_C_20190322_000002",
                           observation_type="flat",
                           physical_filter="SDSSi+ND_OD0.5",
                           pressure=None,
                           relative_humidity=None,
                           science_program="6489D",
                           temperature=None,
                           visit_id=2019032200002)),
                     ("lsstCam-MC_C_20190406_000643_R10_S00.yaml",
                      dict(telescope="LSST",
                           instrument="lsstCam",
                           boresight_rotation_coord="unknown",
                           dark_time=1007.422*u.s,
                           detector_exposure_id=2019040600643027,
                           detector_group="R10",
                           detector_name="S00",
                           detector_num=27,
                           detector_serial="ITL-3800C-145",
                           exposure_id=2019040600643,
                           exposure_time=999.99*u.s,
                           object="UNKNOWN",
                           observation_id="MC_C_20190406_000643",
                           observation_type="flat",
                           physical_filter="950nm+empty",
                           pressure=None,
                           relative_humidity=None,
                           science_program="6549D",
                           temperature=None,
                           visit_id=2019040600643)),
                     )
        for filename, expected in test_data:
            with self.subTest(f"Testing {filename}"):
                self.assertObservationInfoFromYaml(filename, dir=self.datadir, **expected)

    def test_comCam_translator(self):
        test_data = (("comCam-CC_C_20190530_000001_R22_S00.yaml",
                      dict(telescope="LSST",
                           instrument="comCam",
                           boresight_rotation_coord="unknown",
                           dark_time=0.398*u.s,
                           detector_exposure_id=2019053000001000,
                           detector_group="R22",
                           detector_name="S00",
                           detector_num=0,
                           detector_serial="ITL-3800C-229",
                           exposure_id=2019053000001,
                           exposure_time=0.0*u.s,
                           object="UNKNOWN",
                           observation_id="CC_C_20190530_000001",
                           observation_type="bias",
                           physical_filter="NONE",
                           pressure=None,
                           relative_humidity=None,
                           science_program="unknown",
                           temperature=None,
                           visit_id=2019053000001)),
                     )
        for filename, expected in test_data:
            with self.subTest(f"Testing {filename}"):
                self.assertObservationInfoFromYaml(filename, dir=self.datadir, **expected)

    def test_phosim_translator(self):
        test_data = (("phosim-lsst_a_204595_f3_R11_S02_E000.yaml",
                      dict(telescope="LSST",
                           instrument="PhoSim",
                           boresight_rotation_coord="sky",
                           dark_time=30.0*u.s,
                           detector_exposure_id=204595038,
                           detector_group="R11",
                           detector_name="S02",
                           detector_num=38,
                           detector_serial="R11_S02",
                           exposure_id=204595,
                           exposure_time=30.0*u.s,
                           object="UNKNOWN",
                           observation_id="204595",
                           observation_type="science",
                           physical_filter="i",
                           pressure=520.0*cds.mmHg,
                           relative_humidity=40.0,
                           science_program="204595",
                           temperature=20.0*u.deg_C,
                           visit_id=204595,
                           wcs_params=dict(max_sep=3000.))),  # 2022
                     )
        for filename, expected in test_data:
            with self.subTest(f"Testing {filename}"):
                # PhoSim data are in the future and Astropy complains
                # about astrometry errors.
                with self.assertWarns(astropy.utils.exceptions.AstropyWarning):
                    self.assertObservationInfoFromYaml(filename, dir=self.datadir, **expected)

    def test_latiss_translator(self):
        test_data = (("latiss-2018-09-20-05700065-det000.yaml",
                      dict(telescope="LSSTAuxTel",
                           instrument="LATISS",
                           boresight_rotation_coord="unknown",
                           dark_time=27.0*u.s,
                           detector_exposure_id=2018092000065,
                           detector_group="RXX",
                           detector_name="S00",
                           detector_num=0,
                           detector_serial="ITL-3800C-098",
                           exposure_id=2018092000065,
                           exposure_time=27.0*u.s,
                           object="UNKNOWN",
                           observation_id="AT_C_20180920_000065",
                           observation_type="unknown",
                           physical_filter="NONE",
                           pressure=None,
                           relative_humidity=None,
                           science_program="unknown",
                           temperature=None,
                           visit_id=2018092000065,
                           )),
                     ("latiss-AT_O_20190329_000022-ats-wfs_ccd.yaml",
                      dict(telescope="LSSTAuxTel",
                           instrument="LATISS",
                           boresight_rotation_coord="unknown",
                           dark_time=0.0*u.s,
                           detector_exposure_id=2019032900022,
                           detector_group="RXX",
                           detector_name="S00",
                           detector_num=0,
                           detector_serial="ITL-3800C-098",
                           exposure_id=2019032900022,
                           exposure_time=0.0*u.s,
                           object="UNKNOWN",
                           observation_id="AT_O_20190329_000022",
                           observation_type="bias",
                           physical_filter="NONE",
                           pressure=None,
                           relative_humidity=None,
                           science_program="unknown",
                           temperature=None,
                           visit_id=2019032900022,
                           )),
                     ("latiss-future.yaml",
                      dict(telescope="LSSTAuxTel",
                           instrument="LATISS",
                           boresight_rotation_coord="unknown",
                           dark_time=0.0*u.s,
                           detector_exposure_id=2020032900022,
                           detector_group="RXX",
                           detector_name="S00",
                           detector_num=0,
                           detector_serial="ITL-3800C-098",
                           exposure_id=2020032900022,
                           exposure_time=0.0*u.s,
                           object="UNKNOWN",
                           observation_id="AT_X_20200329_000022",
                           observation_type="bias",
                           physical_filter="NONE",
                           pressure=None,
                           relative_humidity=None,
                           science_program="unknown",
                           temperature=None,
                           visit_id=2020032900022,
                           )),
                     )
        self.assertObservationInfoFromYaml("latiss-future.yaml", dir=self.datadir)
        for filename, expected in test_data:
            with self.subTest(f"Testing {filename}"):
                self.assertObservationInfoFromYaml(filename, dir=self.datadir, **expected)

        # This translation should fail
        with self.assertRaises(KeyError):
            self.assertObservationInfoFromYaml("latiss-future-bad.yaml", dir=self.datadir)

    def test_imsim_translator(self):
        test_data = (("imsim-bias-lsst_a_3010002_R11_S00.yaml",
                      dict(telescope="LSST",
                           instrument="ImSim",
                           boresight_rotation_coord="sky",
                           dark_time=0.0*u.s,
                           detector_exposure_id=3010002036,
                           detector_group="R11",
                           detector_name="S00",
                           detector_num=36,
                           detector_serial="LCA-11021_RTM-000",
                           exposure_id=3010002,
                           exposure_time=0.0*u.s,
                           object="UNKNOWN",
                           observation_id="3010002",
                           observation_type="science",  # The header is wrong
                           physical_filter="i",
                           pressure=None,
                           relative_humidity=40.0,
                           science_program="42",
                           temperature=None,
                           visit_id=3010002,
                           wcs_params=dict(max_sep=3000.),  # 2022
                           )),
                     ("imsim-lsst_a_204595_R11_S02_i.yaml",
                      dict(telescope="LSST",
                           instrument="ImSim",
                           boresight_rotation_coord="sky",
                           dark_time=30.0*u.s,
                           detector_exposure_id=204595038,
                           detector_group="R11",
                           detector_name="S02",
                           detector_num=38,
                           detector_serial="LCA-11021_RTM-000",
                           exposure_id=204595,
                           exposure_time=30.0*u.s,
                           object="UNKNOWN",
                           observation_id="204595",
                           observation_type="science",  # The header is wrong
                           physical_filter="i",
                           pressure=None,
                           relative_humidity=40.0,
                           science_program="204595",
                           temperature=None,
                           visit_id=204595,
                           wcs_params=dict(max_sep=3000.),  # 2022
                           )),
                     ("imsim-flats-lsst_a_5000007_R11_S20_i.yaml",
                      dict(telescope="LSST",
                           instrument="ImSim",
                           boresight_rotation_coord="sky",
                           dark_time=30.0*u.s,
                           detector_exposure_id=5000007042,
                           detector_group="R11",
                           detector_name="S20",
                           detector_num=42,
                           detector_serial="LCA-11021_RTM-000",
                           exposure_id=5000007,
                           exposure_time=30.0*u.s,
                           object="UNKNOWN",
                           observation_id="5000007",
                           observation_type="flat",
                           physical_filter="i",
                           pressure=None,
                           relative_humidity=40.0,
                           science_program="5000007",
                           temperature=None,
                           visit_id=5000007,
                           wcs_params=dict(max_sep=3000.),  # 2022
                           )),
                     ("imsim-dark-lsst_a_4010003_R11_S11.yaml",
                      dict(telescope="LSST",
                           instrument="ImSim",
                           boresight_rotation_coord="sky",
                           dark_time=500.0*u.s,
                           detector_exposure_id=4010003040,
                           detector_group="R11",
                           detector_name="S11",
                           detector_num=40,
                           detector_serial="LCA-11021_RTM-000",
                           exposure_id=4010003,
                           exposure_time=500.0*u.s,
                           object="UNKNOWN",
                           observation_id="4010003",
                           observation_type="science",  # The header is wrong
                           physical_filter="i",
                           pressure=None,
                           relative_humidity=40.0,
                           science_program="42",
                           temperature=None,
                           visit_id=4010003,
                           wcs_params=dict(max_sep=3000.),  # 2022
                           )),
                     )
        for filename, expected in test_data:
            with self.subTest(f"Testing {filename}"):
                # ImSim data are in the future and Astropy complains
                # about astrometry errors.
                if expected["observation_type"] == "science":
                    with self.assertWarns(astropy.utils.exceptions.AstropyWarning):
                        self.assertObservationInfoFromYaml(filename, dir=self.datadir, **expected)
                else:
                    self.assertObservationInfoFromYaml(filename, dir=self.datadir, **expected)

    def test_ts3_translator(self):
        test_data = (("ts3-E2V-CCD250-411_lambda_flat_1000_025_20181115075559.yaml",
                      dict(telescope="LSST",
                           instrument="LSST-TS3",
                           dark_time=44.631*u.s,
                           detector_exposure_id=201811151255111433,
                           detector_group="R433",
                           detector_name="S00",
                           detector_num=433,
                           detector_serial="E2V-CCD250-411",
                           exposure_id=201811151255111,
                           exposure_time=44.631*u.s,
                           observation_id="E2V-CCD250-411_lambda_flat_1000_025_20181115075559",
                           observation_type="flat",
                           physical_filter="550CutOn",
                           science_program="2018-11-15",
                           visit_id=201811151255111)),
                     ("ts3-ITL-3800C-098_lambda_flat_1000_067_20160722020740.yaml",
                      dict(telescope="LSST",
                           instrument="LSST-TS3",
                           dark_time=30.611*u.s,
                           detector_exposure_id=201607220607067071,
                           detector_group="R071",
                           detector_name="S00",
                           detector_num=71,
                           detector_serial="ITL-3800C-098",
                           exposure_id=201607220607067,
                           exposure_time=30.611*u.s,
                           observation_id="ITL-3800C-098_lambda_flat_1000_067_20160722020740",
                           observation_type="flat",
                           physical_filter="550CutOn",
                           science_program="2016-07-22",
                           visit_id=201607220607067)),
                     )
        for filename, expected in test_data:
            with self.subTest(f"Testing {filename}"):
                self.assertObservationInfoFromYaml(filename, dir=self.datadir, **expected)

    def test_ts8_translator(self):
        test_data = (("ts8-E2V-CCD250-179_lambda_bias_024_6006D_20180724104156.yaml",
                      dict(telescope="LSST",
                           instrument="LSST-TS8",
                           dark_time=0.0*u.s,
                           detector_exposure_id=201807241041568067,
                           detector_group="RTM-010",
                           detector_name="S11",
                           detector_num=67,
                           detector_serial="E2V-CCD250-179",
                           exposure_id=201807241041568,
                           exposure_time=0.0*u.s,
                           observation_id="E2V-CCD250-179_lambda_bias_024_6006D_20180724104156",
                           observation_type="bias",
                           physical_filter="y",
                           science_program="6006D",
                           visit_id=201807241041568)),
                     ("ts8-E2V-CCD250-200-Dev_lambda_flat_0700_6006D_20180724102845.yaml",
                      dict(telescope="LSST",
                           instrument="LSST-TS8",
                           dark_time=21.913*u.s,
                           detector_exposure_id=201807241028453065,
                           detector_group="RTM-010",
                           detector_name="S02",
                           detector_num=65,
                           detector_serial="E2V-CCD250-200",
                           exposure_id=201807241028453,
                           exposure_time=21.913*u.s,
                           observation_id="E2V-CCD250-200-Dev_lambda_flat_0700_6006D_20180724102845",
                           observation_type="flat",
                           physical_filter="z",
                           science_program="6006D",
                           visit_id=201807241028453)),
                     ("ts8-E2V-CCD250-220_fe55_fe55_094_6288_20171215114006.yaml",
                      dict(telescope="LSST",
                           instrument="LSST-TS8",
                           dark_time=300.0*u.s,
                           detector_exposure_id=201712151140062027,
                           detector_group="RTM-005",
                           detector_name="S00",
                           detector_num=27,
                           detector_serial="E2V-CCD250-220",
                           exposure_id=201712151140062,
                           exposure_time=300.0*u.s,
                           observation_id="E2V-CCD250-220_fe55_fe55_094_6288_20171215114006",
                           observation_type="fe55",
                           physical_filter="i",
                           science_program="6288",
                           visit_id=201712151140062)),
                     )
        for filename, expected in test_data:
            with self.subTest(f"Testing {filename}"):
                self.assertObservationInfoFromYaml(filename, dir=self.datadir, **expected)

    def test_ucdcam_translator(self):
        test_data = (("UCD-E2V-CCD250-112-04_flat_flat_100_20181205153143.yaml",
                      dict(telescope="LSST",
                           instrument="LSST-UCDCam",
                           dark_time=0.5*u.s,
                           detector_exposure_id=201812052331480,
                           detector_group="R00",
                           detector_name="S00",
                           detector_num=0,
                           detector_serial="E2V-CCD250-112-04",
                           exposure_id=20181205233148,
                           exposure_time=0.5*u.s,
                           observation_id="E2V-CCD250-112-04_flat_flat_100_20181205153143",
                           observation_type="flat",
                           physical_filter="r",
                           science_program="2018-12-05",
                           visit_id=20181205233148)),
                     ("UCD-ITL-3800C-002_flat_flat_100_20180530080354.yaml",
                      dict(telescope="LSST",
                           instrument="LSST-UCDCam",
                           dark_time=0.5*u.s,
                           detector_exposure_id=201805301503552,
                           detector_group="R02",
                           detector_name="S00",
                           detector_num=2,
                           detector_serial="ITL-3800C-002",
                           exposure_id=20180530150355,
                           exposure_time=0.5*u.s,
                           observation_id="ITL-3800C-002_flat_flat_100_20180530080354",
                           observation_type="flat",
                           physical_filter="r",
                           science_program="2018-05-30",
                           visit_id=20180530150355)),
                     )
        for filename, expected in test_data:
            with self.subTest(f"Testing {filename}"):
                self.assertObservationInfoFromYaml(filename, dir=self.datadir, **expected)

    def test_checker(self):
        filename = "latiss-future.yaml"
        from astro_metadata_translator.tests import read_test_file
        from astro_metadata_translator import ObservationInfo
        header = read_test_file(filename, self.datadir)
        obsInfo = ObservationInfo(header, pedantic=True)
        self.assertTrue(obsInfo)


if __name__ == "__main__":
    unittest.main()
