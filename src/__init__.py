"""Package init.

We cap native (OpenMP / BLAS) thread pools to 1 **before** scikit-learn / numpy
are imported anywhere. On constrained or containerised environments, libraries
with internal OpenMP parallelism — notably HistGradientBoosting — can deadlock or
oversubscribe when they try to spin up a thread pool. Forcing a single native
thread avoids that hang. The dataset is tiny (~300 rows), so there is no
meaningful speed cost. Advanced users on a strong machine can override any of
these by exporting the variable before running.
"""
import os as _os

for _var in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
):
    _os.environ.setdefault(_var, "1")
