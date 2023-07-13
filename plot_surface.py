# usr/bin/env python3
import matplotlib.pyplot as plt
import tkinter.filedialog
import pandas as pd
import numpy as np


def csv_line_to_xyz(line: str) -> list[float]:
    line = line.replace("\n", "")
    line = line[0:-1]
    values = [float(value) for value in line.split(",")]
    return values


def main():
    filename = tkinter.filedialog.askopenfilename(initialdir="./Data", filetypes=[("comma separated values", "*.csv")])

    dataframe = pd.read_csv(filename)
    data = np.zeros(shape=(3, int(dataframe["y [mm]"].max()+1), int(dataframe["x [mm]"].max()+1)))
    for row in dataframe.values:
        data[0][int(row[1])][int(row[0])] = row[0]
        data[1][int(row[1])][int(row[0])] = row[1]
        data[2][int(row[1])][int(row[0])] = 50 - row[2]

    plt.style.use("_mpl-gallery")
    figure, axes = plt.subplots(ncols=3, subplot_kw={"projection": "3d"})

    surface = axes[0].plot_surface(*data, cmap="plasma_r", linewidth=0, antialiased=False)

    axes[1].bar3d(data[0].ravel() - .5, data[1].ravel() - .5,
                  np.zeros_like(data[2]).ravel(), np.ones_like(data[2]).ravel(),
                  np.ones_like(data[2]).ravel(), data[2].ravel())

    axes[2].scatter(data[0], data[1], data[2]/2, s=data[2], c=data[2], cmap="plasma_r", alpha=0.03)
    x_center = np.sum(data[2]*data[0])/np.sum(data[2])
    y_center = np.sum(data[2]*data[1])/np.sum(data[2])
    z_center = np.sum(data[2]*(data[2]/2))/np.sum(data[2])
    axes[2].scatter(x_center, y_center, z_center, color='k', marker='+', s=1e4)
    axes[2].set_title(f"Center of mass: ({x_center:.2f}, {y_center:.2f}, {z_center:.2f})\n\u03C1 = const.")

    for axes_ in axes:
        axes_.set_xlabel("x [mm]")
        axes_.set_ylabel("y [mm]")
        axes_.set_zlabel("z [mm]")
        axes_.axis("equal")
    figure.colorbar(surface, ax=axes, shrink=0.6, aspect=20)  # TODO: check if the color-bar is applied to all axes

    plt.show()


if __name__ == "__main__":
    main()
