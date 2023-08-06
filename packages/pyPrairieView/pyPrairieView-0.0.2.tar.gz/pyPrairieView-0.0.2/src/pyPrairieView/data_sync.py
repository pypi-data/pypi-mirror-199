from __future__ import annotations
from typing import List
import numpy as np
import pandas as pd
from xml.etree import ElementTree


""" Library of functions for synchronizing data"""


def _dummy_reader_of_frame_times(filename: str) -> List[float]:  # pragma: no cover
    """

    This is just a dummy reader to stand in for whatever long-term solution exists for full .xml parsing
    """
    tree = ElementTree.parse(filename)
    root = tree.getroot()

    # assert expected
    child_tags = [child.tag for child in root]
    expected_tags = ("SystemIDs", "PVStateShard", "Sequence")

    # for tag_ in expected_tags:
    #   assert (tag_ in child_tags), "XML follows unexpected structure"

    # Since expected, let's grab frame sequence
    sequence = root.find("Sequence")
    # use set comprehension to avoid duplicates
    relative_frame_times = {frame.attrib.get("relativeTime") for frame in sequence if "relativeTime" in frame.attrib}
    # convert to float (appropriate type) & sort chronologically
    return sorted([float(frame) for frame in relative_frame_times])


def sync_data(analog_data: pd.DataFrame, frame_times: List[float], fill: bool = True) -> pd.DataFrame:
    """
    Synchronizes analog data & imaging frames using the timestamp of each frame. Option to generate a second column
    in which the frame index is interpolated such that each analog sample matches with an associated frame.

    :param analog_data: analog data
    :type analog_data: pandas.DataFrame
    :param frame_times: frame timestamps
    :type frame_times: List[float]
    :param fill: whether to include an interpolated column so each sample has an associated frame
    :type fill: bool = True
    :return: synchronized data
    :rtype: pandas.DataFrame
    """
    frames = range(len(frame_times))
    # convert to same type as analog data to avoid people getting gotcha'd by pandas
    frames = np.array(frames, dtype=analog_data.index.to_numpy().dtype)
    # convert to milliseconds, create new array to avoid people getting gotcha'd by pandas
    frame_times_ = np.array(frame_times) * 1000
    # round to each millisecond
    frame_times_ = np.round(frame_times_)
    # match types to analog_data index to avoid gotchas
    frame_times_ = frame_times_.astype(analog_data.index.dtype)
    frame_times_ = pd.Series(data=frames, index=frame_times_, name="Frame")
    frame_times_.index.name = "Time(ms)"
    frame_times_ = frame_times_.reindex(index=analog_data.index)

    # Join frames & analog (deep copy to make sure not a view)
    data = analog_data.copy(deep=True)
    data = data.join(frame_times_)

    if fill:
        frame_times_filled = frame_times_.copy(deep=True)
        frame_times_filled.name = "Frame (filled)"
        frame_times_filled.interpolate(method="nearest", inplace=True)
        # forward fill the final frame
        frame_times_filled.ffill(inplace=True)
        data = data.join(frame_times_filled)

    return data
