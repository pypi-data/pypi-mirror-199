__version__ = "0.1.8"

__all__ = [
    "Assay",
    "load",
]
from magnify.assay import Assay
from magnify.registry import load
import magnify.find
import magnify.preprocess
import magnify.reader
import magnify.segment
import magnify.stitch
