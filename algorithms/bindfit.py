def main(
    data,
    method,
    model,
    params,
    subInitValues,
    dilutionCorrection,
    flavour,
    fitCurve,
    fitResiduals,
    fitMolefractions,
    fitCoefficients,
    fitQuality,
    fitSummary,
):
    """Construct and run a Bindfit fitter given a dataset and parameters

    Parameter space
    ---------------
    data: `tabular-data-resource`
        Tabular input data in array of named row objects format
    method: `str`
        The optimisation algorithm to use for fitting
    model: `str`
        The model to fit to the data
    params: `parameter-tabular-data-resource`
        Table of parameters containing initial guesses and output values
    subInitValues: `bool`
        If true, subtract the first column from all data before fitting
    dilutionCorrection: `bool`
        If true, apply dilution correction to data before fitting
    flavour: `str` or None
        If not None, one of "add", "stat" or "noncoop"
    fitCurve: `tabular-data-resource`
        Output fit curve
    fitResiduals: `tabular-data-resource`
        Output fit residuals
    fitMolefractions: `tabular-data-resource`
        Output fit molefractions

    Returns
    -------
    params: `parameter-tabular-data-resource`
        Table of parameters containing initial guesses and output values
    fitCurve: `tabular-data-resource`
        Optimised fit curve
    fitResiduals: `tabular-data-resource`
        Optimised fit curve residual values
    fitMolefractions: `tabular-data-resource`
        Optimised fit molefractions
    fitCoefficients: `tabular-data-resource`
        Optimised fit coefficients
    fitSummary: `tabular-data-resource`
        A summary of fit information - time to fit, degrees of freedom, etc.
    fitQuality: `tabular-data-resource`
        Quality of fit metrics
    """
    # Imports
    import bindfit

    # Error checks
    if not data:
        raise ValueError("No data passed to algorithm")

    # Convert param initial values and bounds to Bindfit format
    input_params = {}

    for key, row in params.data.iterrows():
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
        data=data.data,
        function=function,
        params=input_params,
        normalise=subInitValues,
        dilution_correction=dilutionCorrection,
    )

    fitter.run_scipy(input_params, method=method)

    # Munge output data

    # Write optimised parameter values
    for key, result in fitter.params.items():
        params.data.loc[key, "value"] = result["value"]
        params.data.loc[key, "stderr"] = result["stderr"]

    # Write output fit and residuals data
    fitCurve.data = fitter.fit_curve
    fitResiduals.data = fitter.fit_residuals

    # Write output molefractions
    fitMolefractions.data = fitter.fit_molefractions

    # Write output coefficients
    fitCoefficients.data = fitter.fit_coefficients

    # Write output fit quality statistics
    fitQuality.data = fitter.fit_quality

    # Write output fit details
    fitSummary.data = fitter.fit_summary

    return {
        "params": params,
        "fitCurve": fitCurve,
        "fitResiduals": fitResiduals,
        "fitMolefractions": fitMolefractions,
        "fitCoefficients": fitCoefficients,
        "fitSummary": fitSummary,
        "fitQuality": fitQuality,
    }
