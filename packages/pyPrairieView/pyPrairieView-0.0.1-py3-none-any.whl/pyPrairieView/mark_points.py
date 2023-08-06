from __future__ import annotations
from xml.etree import ElementTree
from pyPrairieView.bruker_meta_objects import BrukerMeta
from collections import ChainMap
from PPVD.style import TerminalStyle
import numpy as np


class PhotostimulationMeta(BrukerMeta):
    def __init__(self, root: ElementTree, factory: object, width: int = 512, height: int = 512):
        """
        Metadata object for Photostimulation / MarkedPoints Protocols.

        Can either be loaded from an experiment OR built to generate new experiments
        """
        self.sequence = None
        self.rois = []
        self.image_width = width
        self.image_height = height

        super().__init__(root, factory)
        return

    @staticmethod
    def __name__() -> str:
        """
        Abstract dunder method

        """
        return "Photostimulation Metadata"

    def build_meta(self, root: ElementTree, factory: object) -> PhotostimulationMeta:
        """
        Abstract method for building metadata object

        :param root:
        :param factory:
        :return:
        """
        self.sequence = factory.constructor(root)
        self._roi_constructor(root, factory)

    def _roi_constructor(self, root: ElementTree, factory: object) -> PhotostimulationMeta:
        """
        Constructs each ROI

        :param root:
        :param factory:
        :return:
        """
        for roi_ in root:
            roi = []
            for child in roi_.iter():
                roi.append(factory.constructor(child))
            self.rois.append(ROI(*roi))

    def extra_actions(self) -> BrukerMeta:
        for roi in self.rois:
            roi.coordinates = roi.generate_coordinates(self.image_width, self.image_height)

    def generate_protocol(self, path: str) -> None:
        """
        Generates a protocol for the metadata to be imported into prairieview

        :param path: path to write protocol
        :type path: str or pathlib.Path
        :rtype: None
        """
        pass


class ROI:
    """
    ROI Object

    """
    def __init__(self, *args):

        self.coordinates = None

        self.mask = None

        self.parameters = {}

        self._map = ChainMap(*args)

        self.pull_parameters_to_upper_level()

    def pull_parameters_to_upper_level(self):
        params = []
        for parameter_set in self._map.maps:
            params.append(parameter_set.__dict__)
        self.parameters = dict(ChainMap(*params))

    def generate_coordinates(self, width: int, height: int) -> Tuple[float, float]:
        """
        Converts the normalized coordinates to image coordinates

        :param width: width of image
        :type width: int
        :param height: height of image
        :type height: int
        :return:  x,y coordinates
        :rtype: tuple[float, float]
        """
        return self.parameters.get("x") * width, self.parameters.get("y") * height

    def __str__(self):
        """
        Modified dunder method such that the printing is more verbose and easier for human consumption

        Prints the roi and each of its parameters, their values. It skips over the underlying chain map & the mask

        :rtype: str
        """
        string_to_print = ""
        string_to_print += f"\n{self.__name__()}\n"
        for key, value in vars(self).items():
            if isinstance(value, dict):
                string_to_print += f"{TerminalStyle.YELLOW}{TerminalStyle.BOLD}{key}{TerminalStyle.RESET}:"
                for nested_key in vars(self).get(key):
                    string_to_print += f"\n\t{TerminalStyle.YELLOW}{nested_key}: {TerminalStyle.RESET}" \
                                       f"{vars(self).get(key).get(nested_key)}"
                string_to_print += "\n"
            elif isinstance(value, ChainMap):
                pass
            elif isinstance(value, np.ndarray):
                pass
            else:
                string_to_print += f"{TerminalStyle.YELLOW}{TerminalStyle.BOLD}{key}: " \
                                   f"{TerminalStyle.RESET}{vars(self).get(key)}\n"
        return string_to_print

    @staticmethod
    def __name__():
        return "ROI"


def generate_mark_points_protocol(metadata: PhotostimulationMeta):
    pass
