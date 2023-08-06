import pytest
import os
import numpy as np
# noinspection PyProtectedMember
from pyPrairieView.data_sync import sync_data, _dummy_reader_of_frame_times
from pyPrairieView.io_tools import load_voltage_recording
from tests.conftest import xml_dir
import pathlib


DATASET = pytest.mark.datafiles(xml_dir)


@pytest.mark.parametrize("fill_", [True, False])
@DATASET
def test_sync_data(datafiles, fill_):
    # find/load the voltage_recording
    file = [file for file in pathlib.Path(datafiles).glob("*.csv")]
    analog = load_voltage_recording(file[0])
    # find/load frame times
    frame_file = [file for file in pathlib.Path(datafiles).glob("*002.xml")]
    frame_times = _dummy_reader_of_frame_times(frame_file[0])
    # run function
    data = sync_data(analog, frame_times, fill=fill_)
    # check for mutation of original frame times
    with pytest.raises(AssertionError):
        np.testing.assert_equal(np.array(frame_times), data["Frame"].to_numpy())
    # check for sortedness
    np.testing.assert_equal(analog["Photostimulation"].to_numpy(), data["Photostimulation"].to_numpy())
    # check appropriately filled
    if fill_:
        assert (len(data.columns) == len(analog.columns) + 2), "Improper fill"
    else:
        assert (len(data.columns) == len(analog.columns) + 1), "Improper fill"
