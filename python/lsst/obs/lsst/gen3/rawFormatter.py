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

"""Gen3 Butler Formatters for LSST raw data.
"""

__all__ = ("LsstCamRawFormatter", "LatissRawFormatter")

from astro_metadata_translator import fix_header, merge_headers

import lsst.afw.fits
from lsst.obs.base.fitsRawFormatterBase import FitsRawFormatterBase

from .instrument import LsstCamInstrument, LatissInstrument, \
    ImsimInstrument, PhosimInstrument, Ts8Instrument, \
    Ts3Instrument, UcdCamInstrument, LsstComCamInstrument
from ..translators import LsstLatissTranslator, LsstCamTranslator, \
    LsstUCDCamTranslator, LsstTS3Translator, LsstComCamTranslator, \
    PhosimTranslator, LsstTS8Translator, ImsimTranslator
from ..assembly import fixAmpsAndAssemble, readRawAmps


class LsstCamRawFormatter(FitsRawFormatterBase):
    translatorClass = LsstCamTranslator
    filterDefinitions = LsstCamInstrument.filterDefinitions
    _instrument = LsstCamInstrument

    def readMetadata(self):
        """Read all header metadata directly into a PropertyList.

        Specialist version since some of our data does not
        set INHERIT=T so we have to merge the headers manually.

        Returns
        -------
        metadata : `~lsst.daf.base.PropertyList`
            Header metadata.
        """
        file = self.fileDescriptor.location.path
        phdu = lsst.afw.fits.readMetadata(file, 0)
        if "INHERIT" in phdu:
            # Trust the inheritance flag
            return super().readMetadata()

        # Merge ourselves
        md = merge_headers([phdu, lsst.afw.fits.readMetadata(file)],
                           mode="overwrite")
        fix_header(md)
        return md

    def getDetector(self, id):
        return self._instrument.getCamera()[id]

    def readImage(self):
        """Read just the image component of the Exposure.

        Returns
        -------
        image : `~lsst.afw.image.Image`
            In-memory image component.
        """
        return self.readFull().getImage()

    def readFull(self, parameters=None):
        """Read the complete exposure.

        This correctly fixes amplifier bounding box deviations from
        the camera definitions, and so should provide the safest
        interface to the data.

        Parameters
        ----------
        parameters : `dict`, optional
            No parameters are currently used.

        Returns
        -------
        exposure : `~lsst.afw.image.Exposure`
            Complete in-memory exposure representation.

        """
        rawFile = self.fileDescriptor.location.path
        ccd = self.getDetector(self.observationInfo.detector_num)
        ampExps = readRawAmps(rawFile, ccd)
        exposure = fixAmpsAndAssemble(ampExps, rawFile)

        mask = self.readMask()
        if mask is not None:
            exposure.setMask(mask)
        variance = self.readVariance()
        if variance is not None:
            exposure.setVariance(variance)

        info = exposure.getInfo()
        info.setFilter(self.makeFilter())
        info.setVisitInfo(self.makeVisitInfo())
        info.setWcs(self.makeWcs(info.getVisitInfo(), info.getDetector()))

        exposure.setMetadata(self.metadata)

        return exposure


class LatissRawFormatter(LsstCamRawFormatter):
    translatorClass = LsstLatissTranslator
    _instrument = LatissInstrument


class ImsimRawFormatter(LsstCamRawFormatter):
    translatorClass = ImsimTranslator
    _instrument = ImsimInstrument


class PhosimRawFormatter(LsstCamRawFormatter):
    translatorClass = PhosimTranslator
    _instrument = PhosimInstrument


class Ts8RawFormatter(LsstCamRawFormatter):
    translatorClass = LsstTS8Translator
    _instrument = Ts8Instrument


class Ts3RawFormatter(LsstCamRawFormatter):
    translatorClass = LsstTS3Translator
    _instrument = Ts3Instrument


class LsstComCamRawFormatter(LsstCamRawFormatter):
    translatorClass = LsstComCamTranslator
    _instrument = LsstComCamInstrument


class UcdCamRawFormatter(LsstCamRawFormatter):
    translatorClass = LsstUCDCamTranslator
    _instrument = UcdCamInstrument
