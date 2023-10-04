def main(
    data,
    params,
    options,
    outputs,
    **kwargs,
):
    import numpy as np
    import pandas as pd

    import bindfit


    # Convert params to Bindfit format
    # TODO: Modify library to accept Frictionless params format
    bindfit_params = {}

    for key, param in params["data"].items():
        bindfit_params.update({
            key: {
                "init": param["value"],
                "bounds": {
                    "min": param["lowerBound"],
                    "max": param["upperBound"],
                },
            }
        })

    model = params["metadata"]["model"]["name"]

    # Bindfit options
    method = options["data"]["method"]
    normalise = options["data"]["normalise"]
    dilute = options["data"]["dilute"]
    flavour = options["data"]["flavour"]

    # Load data
    # TODO: Split this function out into datapackage-utilities library
    def datapackage_to_dataframe(dp):
        df = pd.DataFrame.from_dict(dp["data"])
        # Reorder columns by schema field order
        cols = [ field["name"] for field in dp["schema"]["fields"] ]
        df = df[cols]
        return df

    df = datapackage_to_dataframe(data)

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
        try:
            outputs["params"]["data"].update({
                key: {
                    "value": param["value"],
                    "stderr": param["stderr"],
                },
            })
        except KeyError:
            # No existing data key, create
            outputs["params"] = {
                "data": {
                    key: {
                        "value": param["value"],
                        "stderr": param["stderr"],
                    },
                },
            }

    # TODO: Think of a better way of doing this?
    # Populate output params schema and metadata from input params
    outputs["params"]["metadata"] = params["metadata"]
    outputs["params"]["schema"] = params["schema"]

    # Translate fitter.fit into JSON for tabular data schema
    # TODO: This should be done by the Bindfit library
    def fit_to_json(data, fit):
        x_fields = [ i["name"] for i in data["schema"]["fields"][:2] ]
        y_fields = [ i["name"] for i in data["schema"]["fields"][2:] ]

        fit_data = []

        for data_row, fit_row in zip(data["data"], fit.T):
            row = {}

            for field in x_fields:
                row[field] = data_row[field]

            for i, field in enumerate(y_fields):
                row[field] = fit_row[i]

            fit_data.append(row)

        return fit_data

    outputs["fit"]["data"] = fit_to_json(data, fitter.fit)
    outputs["fit"]["schema"] = data["schema"]

    outputs["residuals"]["data"] = fit_to_json(data, fitter.fit - data_y)
    outputs["residuals"]["schema"] = data["schema"]

    return outputs
