#!/usr/bin/env python3

import argparse
import json
import os.path
import re
import sys

import dito


def get_args():
    parser = argparse.ArgumentParser(description="Convert colorbrewer colormaps (given as JSON file) into dito colormap files.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--debug", action="store_true", help="If set, show full stack trace for errors.")
    parser.add_argument("-i", "--in-filename", type=str, required=True, help="Name of the JSON file specifying the colorbrewer colormaps.")
    parser.add_argument("-o", "--output-dirname", type=str, required=True, help="Directory in which to save the output files.")
    parser.add_argument("-p", "--print-dir", type=str, required=False, default="\"colormaps\", \"colorbrewer\"", help="The saved filenames will be printed in such a way that they can be copied into the definition of 'dito.data.RESOURCES_FILENAMES'. The value of this argument is used a path definition in the 'os.path.join(RESOURCES_DIR, ...)' part.")
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    # load JSON file
    with open(args.in_filename, "r") as f:
        colorbrewer_data = json.load(fp=f)

    # for each colormap...
    colormap_names = sorted(colorbrewer_data.keys())
    for colormap_name in colormap_names:
        colormap_data = colorbrewer_data[colormap_name]
        colormap_name = colormap_name.lower()

        # use the version with the most anchor colors
        max_key = max(int(key) for key in colormap_data.keys() if key != "type")
        color_strs = colormap_data[str(max_key)]

        # convert it into OpenCV/dito format
        colors = []
        for color_str in color_strs:
            match = re.match(r"^rgb\(([0-9]+),([0-9]+),([0-9]+)\)$", color_str)
            assert match is not None
            color = (int(match.group(3)), int(match.group(2)), int(match.group(1)))
            colors.append(color)
        colormap = dito.create_colormap(colors=colors)

        # save it to file
        out_filename = os.path.abspath(os.path.join(args.output_dirname, "{}.png".format(colormap_name)))
        dito.save(filename=out_filename, image=colormap)
        print("    \"colormap:{}\": os.path.join(RESOURCES_DIR, {}, \"{}.png\"),".format(colormap_name, args.print_dir, colormap_name))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        args = get_args()
        if args.debug:
            raise
        else:
            print("ERROR: {} ({})".format(e, type(e).__name__))
            sys.exit(1)
