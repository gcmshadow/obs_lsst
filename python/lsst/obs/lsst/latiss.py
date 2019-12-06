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
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#
import os.path
import re
import lsst.log
from . import LsstCamMapper, LsstCamMakeRawVisitInfo
from .ingest import LsstCamParseTask
from .translators import LsstLatissTranslator

__all__ = ["LatissMapper", "LatissParseTask"]


class LatissMakeRawVisitInfo(LsstCamMakeRawVisitInfo):
    """Make a VisitInfo from the FITS header of a raw image."""
    metadataTranslator = LsstLatissTranslator


class LatissMapper(LsstCamMapper):
    """The Mapper for the LATISS camera."""

    MakeRawVisitInfoClass = LatissMakeRawVisitInfo

    _cameraName = "latiss"
    yamlFileList = ["latiss/latissMapper.yaml"] + list(LsstCamMapper.yamlFileList)

    def _extractDetectorName(self, dataId):
        return f"{LsstLatissTranslator.DETECTOR_GROUP_NAME}_{LsstLatissTranslator.DETECTOR_NAME}"

    def _computeCcdExposureId(self, dataId):
        """Compute the 64-bit (long) identifier for a CCD exposure.

        Parameters
        ----------
        dataId : `dict`
            Data identifier including dayObs and seqNum.

        Returns
        -------
        id : `int`
            Integer identifier for a CCD exposure.
        """
        if len(dataId) == 0:
            return 0                    # give up.  Useful if reading files without a butler

        if 'visit' in dataId:
            visit = dataId['visit']
        else:
            visit = LsstLatissTranslator.compute_exposure_id(dataId['dayObs'], dataId["seqNum"])

        if "detector" in dataId:
            detector = dataId["detector"]
            if detector != 0:
                lsst.log.Log.getLogger("LatissMapper").warn("Got detector %d for LATISS when it should"
                                                            " always be 0", detector)
        else:
            detector = 0

        return LsstLatissTranslator.compute_detector_exposure_id(visit, detector)


class LatissParseTask(LsstCamParseTask):
    """Parser suitable for LATISS raw data.
    """

    _mapperClass = LatissMapper
    _translatorClass = LsstLatissTranslator

    def translate_seqNum(self, md):
        """Return the sequence number.

        Parameters
        ----------
        md : `~lsst.daf.base.PropertyList` or `~lsst.daf.base.PropertySet`
            Image metadata.

        Returns
        -------
        seqnum : `int`
            The sequence number identifier valid within a day.
        """

        if "SEQNUM" in md:
            return md.getScalar("SEQNUM")
        #
        # Oh dear.  Extract it from the filename
        #
        seqNum = 0
        for k in ("IMGNAME", "FILENAME"):
            if k not in md:
                continue
            name = md.getScalar(k)           # e.g. AT-O-20180816-00008
            # Trim trailing extensions
            name = os.path.splitext(name)[0]

            # Want final digits
            mat = re.search(r"(\d+)$", name)
            if mat:
                seqNum = int(mat.group(1))    # 00008
                break

        if seqNum == 0:
            logger = lsst.log.Log.getLogger('obs.lsst.LatissParseTask')
            logger.warn(
                'Could not determine sequence number. Assuming %d ', seqNum)

        return seqNum
