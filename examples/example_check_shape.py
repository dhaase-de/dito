import dito


def main():
    image_shape = (600, 800, 3)

    shape_defs = [
        "h w 3",
        "... 3",
        "... h w 3",
        "h w 3 ...",
        "... h w 3 ...",
        "h w 3 _ ...",
        "h w 1|3",
        "h w |3",
        "h w -3",
        "h w 1|-3",
        "h w 4",
        "h w 1|",
        "h w 1||3",
        "h w |",
        "h w ||",
        "h w *",
        "h w c=1",
        "h w c=3",
        "h w c=1|3",
        "h w c=2|4",
        "h 3 c=3",
        "",
    ]

    print(f"shape={image_shape}")
    for shape_def in shape_defs:
        try:
            dito.check_shape(image_shape, shape_def)
        except Exception as e:
            status = f"FAIL({type(e).__name__}: {e}"
        else:
            status = "OK"

        print(f"shape_def='{shape_def}': {status}")


if __name__ == "__main__":
    main()
