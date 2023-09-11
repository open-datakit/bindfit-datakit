def main(
    inputData,
    inputParams,
    inputOptions,
    outputs,
    **kwargs,
):
    import numpy as np
    import pandas as pd

    import bindfit


    # Convert params to Bindfit format
    # TODO: Modify library to accept Frictionless params format
    bindfit_params = {}

    for key, param in inputParams["data"].items():
        bindfit_params.update({
            key: {
                "init": param["value"],
                "bounds": {
                    "min": param["lowerBound"],
                    "max": param["upperBound"],
                },
            }
        })

    # Bindfit options
    model = inputOptions["data"]["model"]
    method = inputOptions["data"]["method"]
    normalise = inputOptions["data"]["normalise"]
    dilute = inputOptions["data"]["dilute"]
    flavour = inputOptions["data"]["flavour"]

    # Load data
    # TODO: Split this function out into datapackage-utilities library
    def datapackage_to_dataframe(dp):
        df = pd.DataFrame.from_dict(dp["data"])
        # Reorder columns by schema field order
        cols = [ field["name"] for field in dp["schema"]["fields"] ]
        df = df[cols]
        return df

    df = datapackage_to_dataframe(inputData)

    # Bindfit expects each variable as rows
    data_x = np.transpose(df.iloc[:, :2].to_numpy())
    data_y = np.transpose(df.iloc[:, 2:].to_numpy())

    # Apply dilution correction
    # TODO: Think about where this should go - fitter or function?
    # Or just apply it before the fit?
    if dilute:
        data_y = bindfit.helpers.dilute(data_x[0], data_y)

    function = bindfit.functions.construct(
        model,
        normalise=normalise,
        flavour=flavour,
    )

    fitter = bindfit.fitter.Fitter(
        data_x, data_y, function, normalise=normalise, params=bindfit_params
    )

    fitter.run_scipy(bindfit_params, method=method)

    summary = {
        "fitter": model,
        "fit": {
            "y": fitter.fit,
            "coeffs_raw": fitter.coeffs_raw,
            "coeffs": fitter.coeffs,
            "molefrac_raw": fitter.molefrac_raw,
            "molefrac": fitter.molefrac,
            "params": fitter.params,
            "n_y": np.array(fitter.fit).size,
            "n_params": len(fitter.params) + np.array(fitter.coeffs_raw).size,
        },
        "qof": {
            "residuals": fitter.residuals,
            "ssr": bindfit.helpers.ssr(fitter.residuals),
            "rms": bindfit.helpers.rms(fitter.residuals),
            "cov": bindfit.helpers.cov(data_y, fitter.residuals),
            "rms_total": bindfit.helpers.rms(fitter.residuals, total=True),
            "cov_total": bindfit.helpers.cov(data_y, fitter.residuals, total=True),
        },
        "time": fitter.time,
        "options": {
            "dilute": dilute,
            "normalise": normalise,
            "method": method,
            "flavour": flavour,
        },
    }

    # TODO: This conversion should be moved to Bindfit library
    for key, param in fitter.params.items():
        outputs["outputParams"].update({
            "data": {
                key: {
                    "value": param["value"],
                    "stderr": param["stderr"],
                },
            },
        })

    # Translate fitter.fit into JSON for tabular data schema
    # TODO: This should be done by the Bindfit library
    def fit_to_json(data, fit):
        xFields = [ i["name"] for i in inputData["schema"]["fields"][:2] ]
        yFields = [ i["name"] for i in inputData["schema"]["fields"][2:] ]

        fitData = []

        for dataRow, fitRow in zip(inputData["data"], fit.T):
            row = {}

            for field in xFields:
                row[field] = dataRow[field]

            for i, field in enumerate(yFields):
                row[field] = fitRow[i]

            fitData.append(row)

        return fitData

    outputs["outputFit"]["data"] = fit_to_json(inputData, fitter.fit)
    outputs["outputFit"]["schema"] = inputData["schema"]

    return outputs
