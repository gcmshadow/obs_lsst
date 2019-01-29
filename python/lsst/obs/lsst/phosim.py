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
from . import LsstCamMapper, LsstCamMakeRawVisitInfo
from .ingest import LsstCamParseTask
from .translators import PhosimTranslator

__all__ = ["PhosimMapper", "PhosimParseTask"]


class PhosimRawVisitInfo(LsstCamMakeRawVisitInfo):
    """Make a VisitInfo from the FITS header of a raw image."""
    metadataTranslator = PhosimTranslator


class PhosimMapper(LsstCamMapper):
    """The Mapper for the phosim simulations of the LsstCam."""
    translatorClass = PhosimTranslator
    MakeRawVisitInfoClass = PhosimRawVisitInfo

    _cameraName = "phosim"


class PhosimParseTask(LsstCamParseTask):
    """Parser suitable for phosim data.
    """

    _mapperClass = PhosimMapper

    def translate_filter(self, md):
        """Extract filter from metadata (ignoring for corner-raft chips)

        Parameters
        ----------
        md : `lsst.daf.base.PropertyList or PropertySet`
            image metadata

        Returns
        -------
        filter : `str`
            filter name
        """
        return md.get("FILTER")

    def translate_visit(self, md):
        """Extract visit from metadata (as an int)

        Parameters
        ----------
        md : `lsst.daf.base.PropertyList or PropertySet`
            image metadata

        Returns
        -------
        visit : `int`
            visit number
        """
        return int(md.get("OBSID"))
