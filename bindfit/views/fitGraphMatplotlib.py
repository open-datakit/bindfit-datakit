import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def main(
    data: pd.DataFrame, fit: pd.DataFrame, residuals: pd.DataFrame
) -> Figure:
    # Get data
    index = np.array(list(data.data.index.to_numpy()))
    x = index[:, 1] / index[:, 0]  # guest/host
    y = data.data.to_numpy()
    y_fit = fit.data.to_numpy()
    y_residuals = residuals.data.to_numpy()

    # Upper plot
    fig = plt.figure(1)
    upper_frame = fig.add_axes((0.1, 0.3, 0.8, 0.6))

    plt.plot(x, y, ".b")
    plt.plot(x, y_fit, "-r")

    plt.xlabel("[G]/[H]")
    plt.ylabel(r"$\rho$")

    upper_frame.set_xticklabels([])
    plt.grid()

    # Residuals plot
    fig.add_axes((0.1, 0.1, 0.8, 0.2))
    plt.plot(x, y_residuals, ".r")
    plt.grid()

    plt.xlabel("[G]/[H]")
    plt.ylabel(r"$\rho$")

    # Return current figure
    return plt.gcf()
