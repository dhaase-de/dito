import matplotlib.pyplot as plt
import numpy as np

import dito


def get_plot_image():
    (fig, ax) = plt.subplots()
    xs = list(range(10))
    ys = [x**2 for x in xs]
    ax.plot(xs, ys)
    ax.set_title("Example Plot")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    image = dito.fig_to_image(fig=fig, size=(640, 480))
    return image


def get_scatter_image():
    (fig, ax) = plt.subplots()
    xs = np.linspace(-10.0, 10.0, num=11)
    ys = xs**2.0
    ax.scatter(ys, xs)
    ax.set_title("Scatter Plot")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    image = dito.fig_to_image(fig=fig, size=(640, 480))
    return image


def main():
    # get all plots as NumPy images
    plot_image = get_plot_image()
    scatter_image = get_scatter_image()
    dito.pinfo(
        plot_image=plot_image,
        scatter_image=scatter_image,
    )

    # arrange all images into one
    images = [
        plot_image,
        scatter_image,
    ]
    image_show = dito.stack(images, padding=2, background_color=0)

    # show collage of all plot images
    dito.show(image_show, wait=0, scale=1.0)


if __name__ == '__main__':
    main()
