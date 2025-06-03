import cv2

import dito


def main():
    image = dito.background_checkerboard(size=(800, 450))
    image = dito.as_color(image)

    dito.draw_rectangle(
        image=image,
        point1=dito.tir(200, 200),
        point2=dito.tir(400, 300),
        color=(0, 255, 0),
        thickness=2,
        line_type=cv2.LINE_AA,
    )

    dito.draw_circle(
        image=image,
        center=dito.tir(300, 250),
        radius=30,
        color=(0, 255, 255),
        thickness=cv2.FILLED,
        line_type=cv2.LINE_AA,
        start_angle=45.0,
        end_angle=315.0,
    )

    dito.draw_ring(
        image=image,
        center=dito.tir(650, 150),
        radius1=50,
        radius2=40,
        color=(255, 0, 255),
        thickness=cv2.FILLED,
        line_type=cv2.LINE_AA,
    )

    dito.draw_symbol(
        image=image,
        symbol="y_left",
        position=dito.tir(500, 300),
        radius=32,
        color=(255, 255, 0),
        thickness=4,
        line_type=cv2.LINE_AA,
    )

    dito.show(image, scale=1.0, wait=0)


if __name__ == '__main__':
    main()
