from typing import Union
import numpy as np
import pandas as pd
import multiprocessing as mp

from ._chemivec import _rxn_match, _rxn_smarts_isok
from .options import get_option, set_option, _process_n_jobs

def _convert_to_numpy(arr: Union[np.ndarray, pd.DataFrame, pd.Series, list]) -> np.ndarray:
    # Check the array type and convert everything to numpy
    if isinstance(arr, pd.DataFrame):
        if arr.shape[1] > 1:
            raise ValueError("Input dataframe has more than one column, "
                             "please use Series, 1D Numpy array or single column Dataframe")
        arr = arr.squeeze().to_numpy()
    elif isinstance(arr, pd.Series):
        arr = arr.to_numpy()
    elif isinstance(arr, list):
        arr = np.array(arr, dtype=object)
    elif isinstance(arr, np.ndarray):
        pass
    else:
        raise ValueError("Input array can be from the following types: list, np.ndrray, pd.Series or pd.Dataframe,"
                         f"got {type(arr)} type instead")
    return arr


def rxn_subsearch(arr: Union[np.ndarray, pd.DataFrame, pd.Series, list],
                  query_smarts: str = None,
                  aam_mode: str = "DAYLIGHT-AAM",
                  n_jobs: Union[int, None] = None) -> np.ndarray:
    """
    Vectorized reaction substructure search. Input SMILES array and query SMARTS. Both should
    be reactions, e.g. contains ">>" sign. By default, uses daylight atom-to-atom mapping rules:
    https://www.daylight.com/dayhtml/doc/theory/theory.smarts.html (Section 4.6 Reaction Queries)
    If no atom mapping found in query - atom mappings are ignored. By default, uses all available cores
    for parallel computation. This number can be set globally `chemivec.set_option('n_jobs', 12)`

    Example:
        rxn_subsearch([ '[C:1]=O>>[C:1]O', 'C=O>>CO' ],
                  query_smarts = '[C:1]=O>>[C:1]O'
                  )
        output: array([ True, False])

        rxn_subsearch([ '[C:1]=O>>[C:1]O', 'C=O>>CO' ],
                  query_smarts='C=O>>CO'
                  )
        output: array([ True, True])

    :param arr: input array of reaction SMILES, supported inputs: np.ndarray, pd.DataFrame, pd.Series, list
    :param query_smarts: (str) reaction SMARTS
    :param aam_mode: (str) by defaylt "DAYLIGHT-AAM"
    :param n_jobs: (int) number of threads or parallel computation, max by default
    :return: (np.ndarray[bool]) boolean result as numpy array
    """
    # query smarts
    if query_smarts is None or not query_smarts:
        raise ValueError(f"query_smarts could not be empty or None, should be a SMARTS string")
    if not _rxn_smarts_isok(query_smarts):
        raise ValueError(f"Invalid reaction SMARTS: {query_smarts}")

    # n_jobs
    if n_jobs:
        n_jobs = _process_n_jobs(n_jobs)
    else:
        n_jobs = get_option("n_jobs")

    # input array
    arr = _convert_to_numpy(arr)

    # check array dims
    if arr.ndim != 1:
        raise ValueError(f"Multidimensional input arrays not allowed")

    # empty array
    if arr.shape[0] == 0:
        return np.array([], dtype=bool)

    # check item type
    # first check 'np.str_' because it is subclass of 'str'
    if isinstance(arr[0], np.str_):
        return _rxn_match(arr.astype(object), query_smarts, aam_mode, n_jobs)
    elif isinstance(arr[0], str):
        return _rxn_match(arr, query_smarts, aam_mode, n_jobs)

    raise ValueError(f"Input should be array of python or numpy strings, instead got array of {type(arr[0])}")



