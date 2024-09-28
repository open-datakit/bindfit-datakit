import pandas as pd
import bindfit


def main(
    data: pd.DataFrame,
    method: str,
    model: str,
    inputParams: pd.DataFrame,
    subInitValues: bool,
    dilutionCorrection: bool,
    flavour: str | None,
) -> dict:
    """Construct and run a Bindfit fitter given a dataset and parameters

    Parameter space
    ---------------
    data: `pd.DataFrame`
        Input data
    method: `str`
        The optimisation algorithm to use for fitting
    model: `str`
        The model to fit to the data
    inputParams: `pd.DataFrame`
        Table of parameters containing initial guesses and output values
    subInitValues: `bool`
        If true, subtract the first column from all data before fitting
    dilutionCorrection: `bool`
        If true, apply dilution correction to data before fitting
    flavour: `str` or None
        If not None, one of "add", "stat" or "noncoop"

    Returns
    -------
    outputParams: `pd.DataFrame`
        Table of parameters containing initial guesses and output values
    fit: `pd.DataFrame`
        Optimised fit curve
    residuals: `pd.DataFrame`
        Optimised fit curve residual values
    molefractions: `pd.DataFrame`
        Optimised fit molefractions
    coefficients: `pd.DataFrame`
        Optimised fit coefficients
    quality: `pd.DataFrame`
        Quality of fit metrics
    summary: `pdDataFrame`
        A summary of fit information - time to fit, degrees of freedom, etc.
    """

    # Error checks
    if data.empty:
        raise ValueError("No data passed to algorithm")

    # Convert param initial values and bounds to Bindfit format
    input_params = {}

    for key, row in inputParams.iterrows():
        input_params.update(
            {
                key: {
                    "init": row["init"],
                    "bounds": {
                        "min": row["lowerBound"],
                        "max": row["upperBound"],
                    },
                }
            }
        )

    # Construct and run Bindfit fitter
    function = bindfit.functions.construct(
        model,
        normalise=subInitValues,
        flavour=flavour,
    )

    fitter = bindfit.fitter.Fitter(
        data=data,
        function=function,
        params=input_params,
        normalise=subInitValues,
        dilution_correction=dilutionCorrection,
    )

    fitter.run_scipy(input_params, method=method)

    # Munge output data

    # Write optimised parameter values
    outputParams = pd.DataFrame(
        [
            [key, result["value"], result["stderr"]]
            for key, result in fitter.params.items()
        ],
        columns=["name", "value", "stderr"],
    )

    return {
        "outputParams": outputParams,
        "fit": fitter.fit_curve,
        "residuals": fitter.fit_residuals,
        "molefractions": fitter.fit_molefractions,
        "coefficients": fitter.fit_coefficients,
        "summary": fitter.fit_summary,
        "quality": fitter.fit_quality,
    }
