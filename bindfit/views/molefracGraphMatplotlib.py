import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def main(molefractions: pd.DataFrame) -> Figure:
    # Get data
    index = np.array(list(molefractions.index.to_numpy()))
    x = index[:, 1] / index[:, 0]  # Guest/Host
    y = molefractions.to_numpy()

    plt.plot(x, y, "-b")

    plt.xlabel("[G]/[H]")
    plt.ylabel("Molefractions")

    # Return current figure
    return plt.gcf()
