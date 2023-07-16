# usr/bin/env python3
import matplotlib.pyplot as plt
import tkinter.filedialog
import math
import numpy as np
import scipy
import pandas as pd


def calculate_potential_energy(mass: float, height: float) -> float:
    gravitational_acceleration = 9.81  # m/s^2
    return mass * height * gravitational_acceleration


def calculate_velocity_from_energy(kinetic_energy: float, mass: float) -> float:
    return math.sqrt((kinetic_energy * 2) / mass)


def calculate_volume(x_coordinates: np.ndarray, y_coordinates: np.ndarray, z_coordinates: np.ndarray) -> float:
    """
    z_coordinates is data
    length in mm
    volume in mm^3
    """
    spline = scipy.interpolate.RectBivariateSpline(x_coordinates, y_coordinates, z_coordinates)
    return spline.integral(0, z_coordinates.shape[0], 0, z_coordinates.shape[1])


def get_data_from_csv(filename: str) -> np.ndarray:
    """
    Read data from a CSV file and convert it into a numpy array.

    Params:
        filename (str): The path to the CSV file.

    Returns:
        np.ndarray: A numpy array representing the data extracted from the CSV file.
            The shape of the array is (3, M, N), where M is the maximum value in the 'y [mm]' column plus 1,
            and N is the maximum value in the 'x [mm]' column plus 1.
            The first row represents the x-coordinates of the data points.
            The second row represents the y-coordinates of the data points.
            The third row represents the adjusted values obtained from subtracting the 'z' values from 50.

    Note:
        - The CSV file should have columns named 'x [mm]', 'y [mm]', and 'z' respectively.
        - The 'x [mm]' and 'y [mm]' columns should contain integer values representing coordinates.
        - The 'z' column should contain numerical values representing the heights.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    dataframe = pd.read_csv(filename)
    data = np.zeros(shape=(3, int(dataframe["y [mm]"].max() + 1), int(dataframe["x [mm]"].max() + 1)))
    for row in dataframe.values:
        data[0][int(row[1])][int(row[0])] = row[0]
        data[1][int(row[1])][int(row[0])] = row[1]
        data[2][int(row[1])][int(row[0])] = 50 - row[2]
    return data


def get_center_of_mass(data: np.ndarray) -> tuple:
    """
    Calculate the center of mass for a given dataset.

    Params:
        data (np.ndarray): An array containing the data points.
            The shape of the array should be (3, N), where N is the number of data points.
            The first row represents the x-coordinates of the data points.
            The second row represents the y-coordinates of the data points.
            The third row represents the masses or weights associated with the data points.

    Returns:
        tuple: A tuple containing the x-coordinate, y-coordinate, and z-coordinate of the center of mass.

    Raises:
        ValueError: If the shape of the input array is not (3, N), where N is the number of data points.
    """
    x_center = np.sum(data[2]*data[0])/np.sum(data[2])
    y_center = np.sum(data[2]*data[1])/np.sum(data[2])
    z_center = np.sum(data[2]*(data[2]/2))/np.sum(data[2])
    return x_center, y_center, z_center


def get_center_of_mass_from_level_sand_state():
    ...


def set_equal_axes_and_mm_labels(axes: plt.Axes):
    axes.set_xlabel("x [mm]")
    axes.set_ylabel("y [mm]")
    axes.set_zlabel("z [mm]")
    axes.axis("equal")


def plot_surface(axes: plt.Axes, data: np.ndarray):
    surface = axes.plot_surface(*data, cmap="plasma_r", linewidth=0, antialiased=False)
    set_equal_axes_and_mm_labels(axes)
    return surface


def plot_bar_approximation(axes: plt.Axes, data: np.ndarray):
    bar_approximation = axes.bar3d(data[0].ravel() - .5, data[1].ravel() - .5,
                                   np.zeros_like(data[2]).ravel(), np.ones_like(data[2]).ravel(),
                                   np.ones_like(data[2]).ravel(), data[2].ravel())
    set_equal_axes_and_mm_labels(axes)
    return bar_approximation


def plot_center_of_mass(axes: plt.Axes, data: np.ndarray):
    transparent_scatter = axes.scatter(data[0], data[1], data[2] / 2, s=data[2], c=data[2], cmap="plasma_r", alpha=0.03)
    center_of_mass = get_center_of_mass(data)
    print(f"Center of mass: ({center_of_mass[0]:.2f}, {center_of_mass[1]:.2f}, {center_of_mass[2]:.2f})")
    center_of_mass_marker = axes.scatter(*center_of_mass, color='k', marker='+', s=1e4)
    axes.set_title(f"Center of mass: ({center_of_mass[0]:.2f}, {center_of_mass[1]:.2f}, {center_of_mass[2]:.2f})\n"
                   f"\u03C1 = const.")
    set_equal_axes_and_mm_labels(axes)
    return center_of_mass, transparent_scatter, center_of_mass_marker



def main():
    filename = tkinter.filedialog.askopenfilename(initialdir="./Data", filetypes=[("comma separated values", "*.csv")])

    data = get_data_from_csv(filename)

    plt.style.use("_mpl-gallery")
    figure, axes = plt.subplots(ncols=3, subplot_kw={"projection": "3d"})

    surface = plot_surface(axes[0], data)
    plot_bar_approximation(axes[1], data)
    plot_center_of_mass(axes[2], data)

    figure.colorbar(surface, ax=axes, shrink=0.6, aspect=20)  # TODO: check if the color-bar is applied to all axes

    plt.show()


if __name__ == "__main__":
    main()
