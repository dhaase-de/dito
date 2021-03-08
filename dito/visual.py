import cv2
import numpy as np

import dito.core
import dito.data


def get_colormap(name):
    """
    Returns the colormap specified by `name` as `uint8` NumPy array of size
    `(256, 1, 3)`.
    """
    
    # source 1: non-OpenCV colormaps
    data_key = "colormap:{}".format(name.lower())
    if data_key in dito.data.DATA_FILENAMES.keys():
        return dito.io.load(filename=dito.data.DATA_FILENAMES[data_key])
    
    # source 2: OpenCV colormaps
    full_cv2_name = "COLORMAP_{}".format(name.upper())
    if hasattr(cv2, full_cv2_name):
        return cv2.applyColorMap(src=dito.data.yslope(width=1), colormap=getattr(cv2, full_cv2_name))
    
    # no match
    raise ValueError("Unknown colormap '{}'".format(name))


def is_colormap(colormap):
    """
    Returns `True` iff `colormap` is a OpenCV-compatible colormap.
    
    For this, `colormap` must be a `uint8` array of shape `(256, 1, 3)`, i.e.
    a color image of size `1x256`.
    """
    if not dito.core.is_image(image=colormap):
        return False
    if colormap.dtype != np.uint8:
        return False
    if colormap.shape != (256, 1, 3):
        return False
    return True


def colorize(image, colormap):
    """
    Colorize the `image` using the colormap identified by `colormap_name`.
    """
    if isinstance(colormap, str):
        return cv2.applyColorMap(src=image, userColor=get_colormap(name=colormap))
    elif is_colormap(colormap=colormap):
        return cv2.applyColorMap(src=image, userColor=colormap)
    else:
        raise TypeError("Argument `colormap` must either be a string (the colormap name) or a valid colormap.")


####
#%%% image stacking
####


def stack(images, padding=0, background_color=0, dtype=None, gray=None):
    """
    Stack given images into one image.

    `images` must be a vector of images (in which case the images are stacked
    horizontally) or a vector of vectors of images, defining rows and columns.
    """

    # check argument `images`
    if isinstance(images, (tuple, list)) and (len(images) > 0) and isinstance(images[0], np.ndarray):
        # `images` is a vector of images
        rows = [images]
    elif isinstance(images, (tuple, list)) and (len(images) > 0) and isinstance(images[0], (tuple, list)) and (len(images[0]) > 0) and isinstance(images[0][0], np.ndarray):
        # `images` is a vector of vectors of images
        rows = images
    else:
        raise ValueError("Invalid argument 'images' - must be vector of images or vector of vectors of images")

    # find common data type and color mode
    if dtype is None:
        dtype = dito.core.dtype_common((image.dtype for row in rows for image in row))
    if gray is None:
        gray = all(dito.core.is_gray(image=image) for row in rows for image in row)

    # step 1/2: construct stacked image for each row
    row_images = []
    width = 0
    for (n_row, row) in enumerate(rows):
        # determine row height
        row_height = 0
        for image in row:
            row_height = max(row_height, image.shape[0])
        if n_row == 0:
            row_height += 2 * padding
        else:
            row_height += padding

        # construct image
        row_image = None
        for (n_col, image) in enumerate(row):
            # convert individual image to target data type and color mode
            image = dito.core.convert(image=image, dtype=dtype)
            if gray:
                image = dito.core.as_gray(image=image)
            else:
                image = dito.core.as_color(image=image)

            # add padding
            pad_width = [[padding if n_row == 0 else 0, padding], [padding if n_col == 0 else 0, padding]]
            if not gray:
                pad_width.append([0, 0])
            image = np.pad(array=image, pad_width=pad_width, mode="constant", constant_values=background_color)

            # ensure that image has the height of the row
            gap = row_height - image.shape[0]
            if gap > 0:
                if gray:
                    image_fill = np.zeros(shape=(gap, image.shape[1]), dtype=dtype) + background_color
                else:
                    image_fill = np.zeros(shape=(gap, image.shape[1], 3), dtype=dtype) + background_color
                image = np.vstack(tup=(image, image_fill))

            # add to current row image
            if row_image is None:
                row_image = image
            else:
                row_image = np.hstack(tup=(row_image, image))

        # update max width
        width = max(width, row_image.shape[1])
        row_images.append(row_image)

    # step 2/2: construct stacked image from the row images
    stacked_image = None
    for row_image in row_images:
        # ensure that the row image has the width of the final image
        gap = width - row_image.shape[1]
        if gap > 0:
            if gray:
                image_fill = np.zeros(shape=(row_image.shape[0], gap), dtype=dtype) + background_color
            else:
                image_fill = np.zeros(shape=(row_image.shape[0], gap, 3), dtype=dtype) + background_color
            row_image = np.hstack(tup=(row_image, image_fill))

        # add to final image
        if stacked_image is None:
            stacked_image = row_image
        else:
            stacked_image = np.vstack(tup=(stacked_image, row_image))

    return stacked_image


####
#%%% image visualization
####


def show(image, wait=0, scale=None, normalize_mode=None, normalize_kwargs=dict(), colormap=None, window_name="show", close_window=False, engine=None, **kwargs):
    """
    Show image `I` on the screen.

    If `I` is a list of images or a list of lists of images, they are stacked
    into one image.
    """

    if isinstance(image, np.ndarray):
        # I is an image, use it as it is
        J = image
    elif isinstance(image, (list, tuple)) and (len(I) > 0) and isinstance(I[0], np.ndarray):
        # I is a list of images: auto-stack them into one image
        J = astack(I)
    elif isinstance(I, (list, tuple)) and (len(I) > 0) and isinstance(I[0], (list, tuple)) and (len(I[0]) > 0) and isinstance(I[0][0], np.ndarray):
        # I is a list of lists of images: stack them into one image
        J = stack(I)
    else:
        raise ValueError("Invalid value for parameter `image` ({}) - it must either be (i) an image, (ii) a non-empty list of images or a non-empty list of non-empty lists of images".format(I))

    # normalize intensity values
    if normalize is not None:
        J = dito.core.normalize(image=J, mode=normalize_mode, **normalize_kwargs)

    # convert to 8 bit
    #J = convert(J, "uint8")

    # resize image
    if scale is None:
        # try to find a good scale factor automatically
        (W, H) = dh.gui.screenres()
        if (W is not None) and (H is not None):
            scale = 0.85 * min(H / J.shape[0], W / J.shape[1])
        else:
            scale = 850.0 / max(I.shape)
    J = dito.core.resize(image=J, scale_or_size=scale)

    # apply colormap
    if colormap is not None:
        if isinstance(colormap, str):
            colormap = dito.colormap(name=colormap)
        J = dito.channels.colorize(image=J, colormap_name=colormap)

    # determine how to display the image
    if engine is None:
        # TODO: auto-detect if in notebook, then use IPython as engine
        engine = "cv2"

    if engine == "cv2":
        try:
            cv2.imshow(window_name, J)
            key = cv2.waitKey(wait)
        finally:
            if close_window:
                cv2.destroyWindow(window_name)
    elif engine == "ipython":
        # source: https://gist.github.com/uduse/e3122b708a8871dfe9643908e6ef5c54
        import PIL.Image
        from io import BytesIO
        import IPython.display
        f = BytesIO()
        PIL.Image.fromarray(J).save(f, "png")
        IPython.display.display(IPython.display.Image(data=f.getvalue()))
        key = 0
    else:
        raise RuntimeError("Unsupported engine '{}'".format(engine))

    return key
