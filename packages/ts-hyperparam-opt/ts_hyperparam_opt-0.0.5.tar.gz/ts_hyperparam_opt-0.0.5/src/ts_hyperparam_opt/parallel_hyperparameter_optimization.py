import traceback
from math import sqrt

import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import TimeSeriesSplit
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX


def optimize_hyperparams(hyperparams: list, data, func: str, n_steps=1, n_splits=10, runs_per_split=10):
    '''
    Convenience method for optimizing hyperparameters for time series models
    (especially in Notebooks due to having to import functions to use them parallely).
    Best used in a (parallelized) loop, e.g. with a `ProcessPoolExecutor`
    (e.g. `tqdm.contrib.concurrent.process_map`).
    For this, wrap it into/use like this:

    `if __name__ == '__main__':`
        `freeze_support()`

        `results = process_map(functools.partial(pho.optimize_hyperparams, data=data, func="exp_smoothing"), params_exp_smoothing)`

    Warning: Can be computationally intensive, try with a single combination of `hyperparams` and `runs_per_split=1` first.


    :param hyperparams: A list/dict of one combination of hyperparameters to be tried out (look into the particular function to use for the structure it should have).
    :param data: A DataFrame or Series with a continuous index and one column with the data.
    :param func: String of a supported method (currently: "exp_smoothing", "sarima").
    :param n_steps: How many steps to predict into the future.
    :param n_splits: How many CV splits to make (`len(data)` must be larger than `n_splits*n_steps`).
    :param runs_per_split: How often to repeat the prediction per split (takes average results).
    :return: The result (RMSE) for these hyperparameters.
    '''

    data = data.reset_index(drop=True)
    tscv = TimeSeriesSplit(n_splits = n_splits, test_size=n_steps)

    rmse_split = list()
    for train_index, test_index in tscv.split(data):
        cv_train, cv_test = data.iloc[train_index], data.iloc[test_index]
        rmse = list()
        for i in range(0, runs_per_split):
            try:
                preds = globals()[func](hyperparams, cv_train, n_steps)
            except:
                print(hyperparams)
                traceback.print_exc()
                return

            true_values = cv_test.values
            rmse.append(sqrt(mean_squared_error(true_values, preds)))

        rmse_split.append(np.mean(rmse))

    rmse_all = dict()
    rmse_all[str(hyperparams)] = round(np.mean(rmse_split), 2)
    return rmse_all


def sort_results(results_list):
    '''
    Sort a list of results obtained by using `optimize_hyperparams` in a loop.

    :param results_list: Unsorted results list.
    :return: A sorted list.
    '''
    results_list = [i for i in results_list if i is not None]
    return sorted(results_list, key=lambda k: tuple(k.get(key, "") for key in sorted(k)))


def exp_smoothing(hyperparams, cv_train, n_steps):
    return ExponentialSmoothing(
        cv_train.astype(float),
        seasonal_periods=hyperparams["periods"],
        trend=hyperparams["trend"],
        seasonal=hyperparams["seasonal"],
        damped_trend=hyperparams["damped_trend"],
        use_boxcox=hyperparams["use_boxcox"],
        initialization_method="estimated",
    ).fit(remove_bias=hyperparams["remove_bias"]).simulate(n_steps, repetitions=100, error="mul").mean(axis=1)


def sarima(hyperparams, cv_train, n_steps):
    return SARIMAX(
        cv_train.astype(float),
        order=hyperparams[0],
        seasonal_order=hyperparams[1]
    ).fit().forecast(steps=n_steps)
