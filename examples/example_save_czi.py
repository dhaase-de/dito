import pathlib

import dito
import einops


def main():
    image = dito.usc_sipi_beans()
    data = einops.rearrange(image, "y x c -> c y x 1")

    dito.pinfo(image=image, data=data)

    out_path = pathlib.Path(__file__).parent.joinpath("work", "out.czi")
    dito.save(
        out_path,
        data,
        czi_kwargs=dict(
            extra_dim_names="C",
            channel_names={0: "B", 1: "G", 2: "R"},
            channel_display_settings={
                0: {"color_bgr": (255, 0, 0), "is_enabled": True},
            },
        ),
    )


if __name__ == "__main__":
    main()
