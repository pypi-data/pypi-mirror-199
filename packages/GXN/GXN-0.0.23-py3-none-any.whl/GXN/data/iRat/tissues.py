"""
Load gene expression datasets
-----------------------------

Loads gene expression datasets

Example:
    Test the example by running this file::

        $ python gene_expression.py
"""

__author__ = "Sergio Peignier"
__copyright__ = "Copyright 2019, The Dream5 Project"
__credits__ = ["Sergio Peignier"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Sergio Peignier"
__email__ = "sergio.peignier@insa-lyon.fr"
__status__ = "pre-alpha"

from GXN.data.iRat.configuration import library_folder
from GXN.data.iRat.gene_expression import load_tfs_11_organs_4_stages_gene_expression
from os.path import join
from pandas import read_csv

def load_tissue():
    """
    Load datasets tissues

    Returns:
        pandas.DataFrame: iMouse libraries tissues

    Examples:
        >>> df_tissue = load_tissue()
        >>> df_tissue.head()


    """
    X = load_tfs_11_organs_4_stages_gene_expression()
    del X["Gene Name"]
    tf = load_tfs_cofactors()["Ensembl"]
    tissues = pd.Series([n.split(", ")[-1] for n in X.columns],index=X.columns)
    return tissues

if __name__ == '__main__':
    print("Loading tissues data")
    print(load_tissue())
