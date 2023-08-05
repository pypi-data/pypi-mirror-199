

# Time Series Hyperparameter Optimization (CV + Parallel)

Convenience package for optimizing hyperparameters for Time Series forecasting
using methods like _ExponentialSmoothing_ or _SARIMAX_. Especially useful
for Jupyter Notebooks where parallelization (with e.g. `ProcessPoolExecutor`)
only works when importing the function used in parallel.

## Install it from PyPI

```bash
pip install ts-hyperparam-opt
```

## Usage

```py
from ts-hyperparam-opt import parallel_hyperparameter_optimization as pho

params_sarima = [
    [(1,1,1), (1,1,1,7)],
    [(1,1,0), (1,1,1,7)]
    ]

if __name__ == '__main__':
    freeze_support()
    results = process_map(functools.partial(pho.optimize_hyperparams,
                            data=df_data, func="sarima", 
                            n_steps=15), params_sarima)
    results_sorted = pho.sort_results(results)
```

## Development

Alpha Version

Currently supported methods:
- (Triple) Exponential Smoothing (Holt-Winters)
- SARIMA(X)