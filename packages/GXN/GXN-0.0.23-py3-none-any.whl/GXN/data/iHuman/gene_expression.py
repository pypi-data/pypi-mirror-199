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

from GXN.data.iHuman.configuration import library_folder
from GXN.data.iHuman.tf import load_tfs_cofactors
from os.path import join
from pandas import read_csv

def load_sensory_neurons_IPS(gene_name_as_id = False):
    """
    Load the sensory_neurons_IPS human dataset

    Returns:
        pandas.DataFrame: gene expression dataset
        rows represent genes and columns represent conditions

    Examples:


    """
    expr_data = read_csv(join(library_folder,"sensory_neurons_IPS", "E-ENAD-33-query-results.tpms.tsv"),
                         header=0,
                         index_col=0,
                         comment="#",
                         sep="\t")
    if gene_name_as_id:
        expr_data.index = expr_data["Gene Name"]
        del expr_data["Gene Name"]
    # replace row index with corresponding value in dictionary
    return expr_data.fillna(0)

def load_tfs_sensory_neurons_IPS():
    """
    Load in mouse TFs dataset

    Returns:
        pandas.DataFrame: iDog TFs gene expression dataset
        rows represent genes and columns represent conditions

    Examples:


    """
    X = load_sensory_neurons_IPS()
    tfs = load_tfs_cofactors()["Ensembl"]
    X_tfs = X.loc[set(tfs).intersection(X.index)]
    return X_tfs

def load_macrophage_immune_response(gene_name_as_id = False):
    """
    Load the macrophage immune response human dataset

    Returns:
        pandas.DataFrame: gene expression dataset
        rows represent genes and columns represent conditions

    Examples:


    """
    expr_data = read_csv(join(library_folder,"macrophage_immune_response", "E-ENAD-41-query-results.tpms.tsv"),
                         header=0,
                         index_col=0,
                         comment="#",
                         sep="\t")
    if gene_name_as_id:
        expr_data.index = expr_data["Gene Name"]
        del expr_data["Gene Name"]
    # replace row index with corresponding value in dictionary
    return expr_data.fillna(0)

def load_tfs_macrophage_immune_response():
    """
    Load macrophage immune response TFs dataset

    Returns:
        pandas.DataFrame: iDog TFs gene expression dataset
        rows represent genes and columns represent conditions

    Examples:


    """
    X = load_macrophage_immune_response()
    tfs = load_tfs_cofactors()["Ensembl"]
    X_tfs = X.loc[set(tfs).intersection(X.index)]
    return X_tfs


def load_Human_developmental_biology_resource(gene_name_as_id = False):
    """
    Load the Human_developmental_biology human dataset

    Returns:
        pandas.DataFrame: gene expression dataset
        rows represent genes and columns represent conditions

    Examples:


    """
    expr_data = read_csv(join(library_folder,"Human_developmental_biology_resource", "E-MTAB-4840-query-results.tpms.tsv"),
                         header=0,
                         index_col=0,
                         comment="#",
                         sep="\t")
    if gene_name_as_id:
        expr_data.index = expr_data["Gene Name"]
        del expr_data["Gene Name"]
    # replace row index with corresponding value in dictionary
    return expr_data.fillna(0)

def load_tfs_Human_developmental_biology_resource():
    """
    Load Human_developmental_biology TFs dataset

    Returns:
        pandas.DataFrame: TFs gene expression dataset
        rows represent genes and columns represent conditions

    Examples:

    """
    X = load_Human_developmental_biology_resource()
    tfs = load_tfs_cofactors()["Ensembl"]
    X_tfs = X.loc[set(tfs).intersection(X.index)]
    return X_tfs




def load_GTEX(gene_name_as_id = False):
    """
    Load the GTEX human dataset

    Returns:
        pandas.DataFrame: gene expression dataset
        rows represent genes and columns represent conditions

    Examples:


    """
    expr_data = read_csv(join(library_folder,"GTEX", "E-MTAB-5214-query-results.tpms.tsv"),
                         header=0,
                         index_col=0,
                         comment="#",
                         sep="\t")
    if gene_name_as_id:
        expr_data.index = expr_data["Gene Name"]
        del expr_data["Gene Name"]
    # replace row index with corresponding value in dictionary
    return expr_data.fillna(0)

def load_tfs_GTEX():
    """
    Load GTEX TFs dataset

    Returns:
        pandas.DataFrame: TFs gene expression dataset
        rows represent genes and columns represent conditions

    Examples:

    """
    X = load_GTEX()
    tfs = load_tfs_cofactors()["Ensembl"]
    X_tfs = X.loc[set(tfs).intersection(X.index)]
    return X_tfs






def load_934_cancer_cell_encyclopedia(gene_name_as_id = False):
    """
    Load the 934_cancer_cell_encyclopedia human dataset

    Returns:
        pandas.DataFrame: gene expression dataset
        rows represent genes and columns represent conditions

    Examples:


    """
    expr_data = read_csv(join(library_folder,"934_cancer_cell_encyclopedia", "E-MTAB-2770-query-results.tpms.tsv"),
                         header=0,
                         index_col=0,
                         comment="#",
                         sep="\s")
    if gene_name_as_id:
        expr_data.index = expr_data["Gene Name"]
        del expr_data["Gene Name"]
    # replace row index with corresponding value in dictionary
    return expr_data.fillna(0)

def load_tfs_934_cancer_cell_encyclopedia():
    """
    Load 934_cancer_cell_encyclopedia TFs dataset

    Returns:
        pandas.DataFrame: TFs gene expression dataset
        rows represent genes and columns represent conditions

    Examples:

    """
    X = load_934_cancer_cell_encyclopedia()
    tfs = load_tfs_cofactors()["Ensembl"]
    X_tfs = X.loc[set(tfs).intersection(X.index)]
    return X_tfs


def load_934_cancer_cell_encyclopedia(gene_name_as_id = False):
    """
    Load the 934_cancer_cell_encyclopedia human dataset

    Returns:
        pandas.DataFrame: gene expression dataset
        rows represent genes and columns represent conditions

    Examples:


    """
    expr_data = read_csv(join(library_folder,"934_cancer_cell_encyclopedia", "E-MTAB-2770-query-results.tpms.tsv"),
                         header=0,
                         index_col=0,
                         comment="#",
                         sep="\s")
    if gene_name_as_id:
        expr_data.index = expr_data["Gene Name"]
        del expr_data["Gene Name"]
    # replace row index with corresponding value in dictionary
    return expr_data.fillna(0)

def load_tfs_934_cancer_cell_encyclopedia():
    """
    Load 934_cancer_cell_encyclopedia TFs dataset

    Returns:
        pandas.DataFrame: TFs gene expression dataset
        rows represent genes and columns represent conditions

    Examples:

    """
    X = load_934_cancer_cell_encyclopedia()
    tfs = load_tfs_cofactors()["Ensembl"]
    X_tfs = X.loc[set(tfs).intersection(X.index)]
    return X_tfs
def load_465_lymphoblastoid_cell_lines(gene_name_as_id = False):
    """
    Load the 465_lymphoblastoid_cell_lines human dataset

    Returns:
        pandas.DataFrame: gene expression dataset
        rows represent genes and columns represent conditions

    Examples:


    """
    expr_data = read_csv(join(library_folder,"465_lymphoblastoid_cell_lines", "E-GEUV-1-query-results.tpms.tsv"),
                         header=0,
                         index_col=0,
                         comment="#",
                         sep="\t")
    if gene_name_as_id:
        expr_data.index = expr_data["Gene Name"]
        del expr_data["Gene Name"]
    # replace row index with corresponding value in dictionary
    return expr_data.fillna(0)

def load_tfs_465_lymphoblastoid_cell_lines():
    """
    Load 465_lymphoblastoid_cell_lines TFs dataset

    Returns:
        pandas.DataFrame: TFs gene expression dataset
        rows represent genes and columns represent conditions

    Examples:

    """
    X = load_465_lymphoblastoid_cell_lines()
    tfs = load_tfs_cofactors()["Ensembl"]
    X_tfs = X.loc[set(tfs).intersection(X.index)]
    return X_tfs

def load_allen_aging_dementia_tbi_study(normalized=True,all_expressed_only=False):

    folder_allen = join(library_folder,
                        "BRAIN",
                        "gene_expression_matrix_2016-03-03")
    if normalized:
        if all_expressed_only:
            expr_data = read_csv(join(folder_allen,
                                     'fpkm_table_normalized_all_expressed.csv.zip'),
                                 index_col=0,)
        else:
            expr_data = read_csv(join(folder_allen,'fpkm_table_normalized.csv'),
                                 index_col=0,)
    else:
        expr_data = read_csv(join(folder_allen,'fpkm_table_unnormalized.csv'),
                             index_col=0,)
    if not all_expressed_only:
        genes_info = read_csv(join(folder_allen,'rows-genes.csv'))
        libraries_info  = read_csv(join(folder_allen,'columns-samples.csv'))
        expr_data.index = genes_info["gene_symbol"]
    return expr_data


if __name__ == '__main__':
    print("Loading gene expression data")
    print(load_gene_expression().head())
