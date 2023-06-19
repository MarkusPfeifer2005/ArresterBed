import matplotlib.pyplot as plt
import tkinter.filedialog


def main():
    plt.style.use("_mpl-gallery")
    figure, axis = plt.subplots(subplot_kw={"projection": "3d"})
    filename = tkinter.filedialog.askopenfilename(initialdir="./Data")
    with open(filename, 'r') as csv_file:
        dataframe = [[] for i in range(3)]
        for line_number, line in enumerate(csv_file.readlines()):
            if line_number == 0:
                continue
            line = line.replace("\n", "")
            line = line[0:-1]
            values = line.split(",")
            for slot, value in zip(dataframe, values):
                slot.append(float(value))
    dataframe[2] = [50 - distance for distance in dataframe[2]]
    surface = axis.plot_trisurf(*dataframe, cmap="plasma")
    axis.set_xlabel("X")
    axis.set_ylabel("Y")
    axis.set_zlabel("Z")
    plt.axis('equal')
    figure.colorbar(surface, ax=axis)
    plt.show()


if __name__ == "__main__":
    main()
