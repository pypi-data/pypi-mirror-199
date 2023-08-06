import contextlib
import joblib
from tqdm import tqdm


@contextlib.contextmanager
def tqdm_joblib(tqdm_object: tqdm):
    """Context manager to patch joblib to report into tqdm progress bar given as argument
    ref: https://stackoverflow.com/a/58936697
    Usage:
    >>> from math import sqrt
    >>> from joblib import Parallel, delayed
    >>> with tqdm_joblib(tqdm(desc="My calculation", total=10)) as progress_bar:
    >>>     Parallel(n_jobs=16)(delayed(sqrt)(i**2) for i in range(10))
    """
    class TqdmBatchCompletionCallback(joblib.parallel.BatchCompletionCallBack):
        def __call__(self, *args, **kwargs):
            tqdm_object.update(n=self.batch_size)
            return super().__call__(*args, **kwargs)

    old_batch_callback = joblib.parallel.BatchCompletionCallBack
    joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallback
    try:
        yield tqdm_object
    finally:
        joblib.parallel.BatchCompletionCallBack = old_batch_callback
        tqdm_object.close()


def phy_cpu_count() -> int:
    return joblib.cpu_count(True)
