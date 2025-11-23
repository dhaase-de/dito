import dito

def main():
    image = dito.dito_test_image_v1()
    dito.show(image, engine="napari")


if __name__ == '__main__':
    main()