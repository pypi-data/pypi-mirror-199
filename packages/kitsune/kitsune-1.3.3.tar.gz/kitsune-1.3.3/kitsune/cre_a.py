"""
.. module:: cre
   :platform: Unix, MacOSX
   :synopsis: module for Cumulative Relative Entropy (CRE) calculation

.. moduleauthor:: Natapol Pornputtapong <natapol.p@chula.ac.th>


"""
from . import kitsunejf as jf
import math
from tqdm import tqdm

def cal_cre(fsa, k, **karg):
    """ Calculate Cumulative Relative Entropy (CRE)
        CRE = sum(RE from kmer to infinite)
    Args:
        fsa genome file in fasta format
        kend the infinite kmer
        kfrom calculate to (defualt=4)

    Returns: dict(kmer: CRE)

    """

    kend = 1 if 
    for kmer in tqdm(range(, kfrom-1, -1)):