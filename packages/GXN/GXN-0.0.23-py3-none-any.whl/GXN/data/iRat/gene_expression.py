"""
Load gene expression datasets
-----------------------------

Loads gene expression datasets

Example:
    Test the example by running this file::

        $ python gene_expression.py
"""

__author__ = "Sergio Peignier"
__copyright__ = "Copyright 2019, The mouse Project"
__credits__ = ["Sergio Peignier"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Sergio Peignier"
__email__ = "sergio.peignier@insa-lyon.fr"
__status__ = "pre-alpha"

from GXN.data.iRat.configuration import library_folder
from GXN.data.iRat.tf import load_tfs_cofactors
from os.path import join
from pandas import read_csv

def load_11_organs_4_stages_gene_expression(gene_name_as_id = False):
    """
    Load in 73 mutatns mouse dataset

    Returns:
        pandas.DataFrame: iDog gene expression dataset
        rows represent genes and columns represent conditions

    Examples:

    """
    expr_data = read_csv(join(library_folder,"eleven_organs_four_stages", "E-GEOD-53960-query-results.tpms.tsv"),
                         header=0,
                         index_col=0,
                         comment="#",
                         sep="\t")
    if gene_name_as_id:
        expr_data.index = expr_data["Gene Name"]
        del expr_data["Gene Name"]
    # replace row index with corresponding value in dictionary
    return expr_data.fillna(0)

def load_tfs_11_organs_4_stages_gene_expression():
    """
    Load in mouse TFs dataset

    Returns:
        pandas.DataFrame: iDog TFs gene expression dataset
        rows represent genes and columns represent conditions

    Examples:


    """
    X = load_11_organs_4_stages_gene_expression()
    tfs = load_tfs_cofactors()["Ensembl"]
    X_tfs = X.loc[set(tfs).intersection(X.index)]
    return X_tfs


if __name__ == '__main__':
    print("Loading gene expression data")
    print(load_gene_expression().head())
