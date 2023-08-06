"""
Code here imports PrairieView generated XML files and extracts the useful information contained inside. 
"""
from io import BufferedReader
import pathlib
import os
import time
import numpy as np

from typing import Union, List, Tuple

class PrairieXML:
    def __init__(self, 
                 xml_file_path: Union[str, pathlib.Path],
                 load_data: bool = True
                 ):
        """
        Load data from an XML file.

        Parameters
        ----------
        xml_file_path : Union[str, pathlib.Path]
            Path to the XML file.
        load_data : bool, optional
            Whether to load XML data. The default is True.
         : TYPE
            DESCRIPTION.

        Returns
        -------
        BrukerMetadata

        """
        if (isinstance(xml_file_path, pathlib.Path)):
            xml_file_path = str(xml_file_path)
        if (os.path.isdir(xml_file_path)):
            raise Exception("path must be a path to a FILE not a FOLDER.")
         
        if not os.path.exists(self.xml_file_path):
            raise ValueError("XML file does not exist: %s" % self.xml_file_path)
        self.abfID = os.path.splitext(os.path.basename(self.xml_file_path))[0]
        with open(self.xml_file_path, 'rb') as fb:

            # The first 4 bytes of the ABF indicates what type of file it is
            self.abfVersion = {}
            fb.seek(0)
            fileSignature = fb.read(4).decode("ascii", errors='ignore')
            if fileSignature == "XML ":
                self.abfVersion["major"] = 1
                self._readHeadersV1(fb)
            elif fileSignature == "ABF2":
                self.abfVersion["major"] = 2
                self._readHeadersV2(fb)
            else:
                raise NotImplementedError("Invalid ABF file format")
        
            # create more local variables based on the header data
            self._makeAdditionalVariables()
        
            # note the file size
            fb.seek(0, os.SEEK_END)
            self._fileSize = fb.tell()
        
            # optionally load data from disk
            if self._preLoadData:
                self._loadAndScaleData(fb)
                self.setSweep(0)
            