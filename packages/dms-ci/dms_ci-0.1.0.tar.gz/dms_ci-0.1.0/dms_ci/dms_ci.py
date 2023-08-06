from .src import wilson

def dms_ci(p, n, z = 1.96):
    """Provides confidence intervals for DMS-MaPseq data.

    Parameters
    ----------

    N : array_like
        Number of reads for each position.

    n : array_like
        Number of mutations for each position.

    alpha : float, optional
        Significance level of the confidence interval. Default is 0.05.

    Returns
    -------

    low : array_like
        Lower confidence interval.

    high : array_like
        Upper confidence interval.

    Notes
    -----

    The confidence intervals are calculated using the Wilson score interval. The bias correction is set to 1E-3, to balance for the substitution errors in the sequencing. 

    """
    
    return wilson(p, n, z, bias_correction=1E-3)
    