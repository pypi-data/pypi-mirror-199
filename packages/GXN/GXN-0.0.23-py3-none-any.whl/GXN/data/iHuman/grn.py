"""
mouse TF datasets
------------------

This module allows to load the GRN for the mouse dataset
To use this library you should also have the related datasets.

Example:
    Test the example by running this file::

        $ python grn.py

Todo:

"""




__author__ = "Sergio Peignier"
__copyright__ = "Copyright 2019, The mouse Project"
__credits__ = ["Sergio Peignier"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Sergio Peignier"
__email__ = "sergio.peignier@insa-lyon.fr"
__status__ = "pre-alpha"

from os.path import join
from pandas import read_csv,concat
from iHuman.configuration import library_folder
from os.path import join
from pandas import read_csv

def load_kegg_GRN():
    grn = read_csv(join(library_folder,"new_kegg.human.reg.direction.txt"),header=0,sep="\s")
    return grn[["TF","Target","Up_or_Down_or_Unknown"]]


if __name__ == '__main__':
    print("Loading GRN data")
    print(load_kegg_GRN())
