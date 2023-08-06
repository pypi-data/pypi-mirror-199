from sys import path
from pathlib import Path
path.append(str(Path(__file__).parent.resolve()))
from IDA import read_image
from skimage.transform import resize
from skimage.util import img_as_ubyte, invert
from numpy import full, array, ndarray, asarray, zeros, amin, amax, clip
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageOps import scale
from typing import List

from MMCQ import palette
from ImageCreation import image


def _DEV_formatting(img: ndarray, pix_limit: int, img_w: int, img_h: int, img_c: int, img_d: str) -> ndarray:
    """
    USED FOR DEVELOPMENT NEEDS: IF YOU DON`T KNOW WHAT YOU`RE DOING, DON`T TOUCH IT
    Formatting algorithm for a image, will resize it to fit the pix limit, delete/convert data
    Input:
    :param img: input image (numpy array) to reformat
    :param pix_limit: limit of pixels for the reformatted image
    :param img_w: width of the image
    :param img_h: height of the image
    :param img_c: amount of channels of the image
    :param img_d: dtype of the image
    Output:
    A image in numpy array form
    Intended for faster processing in MMCQ algorithm, also converting data to one standard (RGB uint8)
    """

    img_d = img.dtype
    if img_w * img_h >= pix_limit:
        m = (pix_limit / (img_w * img_h)) ** 0.5
        img_h = int(img.shape[0] * m)
        img_w = int(img.shape[1] * m)
        img = resize(img, (img_h, img_w), preserve_range=True)
        img = asarray(img, dtype=img_d)
        if img_d == 'uint8' and img_c == 3:
            return img

    if img_c == 4:
        new_img = zeros((img_h, img_w, 3), dtype=img_d)
        new_img[:, :, 0] = img[:, :, 0]
        new_img[:, :, 1] = img[:, :, 1]
        new_img[:, :, 2] = img[:, :, 2]
        img = new_img
    elif img_c == 2:
        new_img = zeros((img_h, img_w, 3), dtype=img_d)
        new_img[:, :, 0] = img[:, :, 0]
        new_img[:, :, 1] = img[:, :, 1]
        new_img[:, :, 2] = img[:, :, 0]
        img = new_img

    if img_d == 'uint8':
        pass
    elif img_d == 'bool':
        img = img_as_ubyte(img)
        img = invert(img)
        row, col = img.shape
        v = img
        new_img = zeros((img_h, img_w, 3), dtype='uint8')
        new_img[:, :, 0] = v
        new_img[:, :, 1] = v
        new_img[:, :, 2] = v
        img = asarray(new_img, dtype='uint8')
    elif img_d in ('float16', 'float32', 'float64'):
        if amax(img) >= 1 or amin(img) < 0:
            img = clip(img, a_min=0, a_max=1)
        img = img_as_ubyte(img)
    else:
        img = img_as_ubyte(img)
    return img


def _DEV_draw_palette(RGB_pal: List[List[int]], cube_side: int = 2, cube_interval: int = 1,
                bg_col: List[int] = [255, 255, 255], scale_size: int = 50) -> ndarray:

    """
    USED FOR DEVELOPMENT NEEDS: IF YOU DON`T KNOW WHAT YOU`RE DOING, DON`T TOUCH IT
    Palette preview algorithm
    :param RGB_pal:list of lists of colors in RGB uint8 format ([[5,5,5],[6,6,6],[7,7,7]] for example)
    :param cube_side: defines cube`s side
    :param cube_interval: defines interval between cubes and surroundings
    :param bg_col: color of a background of the image
    :param scale_size: a parameter, on which the drawing will be scaled after creating palette
    Output:
    An image of the palette in numpy array form
    Intended for saving on hard drive via skimage.io.imsave method
    """

    img_height = cube_side + cube_interval * 2
    img_width = len(RGB_pal) * cube_side + (len(RGB_pal) + 1) * cube_interval

    bg = image(full((img_height, img_width, 3), bg_col, dtype='uint8'))

    c_cube_MAIN = image(full((cube_side, cube_side, 3), RGB_pal[0], dtype='uint8'))
    c_cube_MAIN.translate((cube_interval, cube_interval))
    c_cube_MAIN_ALPHA = c_cube_MAIN.get_alpha()

    pre_comp = image.merge(bg, c_cube_MAIN, c_cube_MAIN_ALPHA)

    for i in range(1, len(RGB_pal)):
        c_cubeN = image(full((cube_side, cube_side, 3), RGB_pal[i], dtype='uint8'))
        c_cubeN.translate((cube_interval, cube_interval))
        c_cubeN.translate(((cube_interval + cube_side) * i, 0))
        c_cubeN_ALPHA = c_cubeN.get_alpha()
        pre_comp = image.merge(pre_comp, c_cubeN, c_cubeN_ALPHA)

    img = Image.fromarray(image.convert_to_numpy(pre_comp, img_width))
    img = scale(img, scale_size, resample=Image.Resampling.NEAREST)
    font = ImageFont.truetype("arial.ttf", cube_interval * int(scale_size / 2))
    drawer = ImageDraw.Draw(img)
    for i in range(len(RGB_pal)):
        drawer.text(((cube_interval * (i + 1) + cube_side * i) * scale_size, int((cube_interval / 2 - .2) * scale_size)), "Color " + str(i + 1) + ":", font=font, fill='black')

    return array(img)


def _DEV_comp_palette_with_picture(img: ndarray, RGB_palette: List[List[int]]) -> ndarray:
    """
    USED FOR DEVELOPMENT NEEDS: IF YOU DON`T KNOW WHAT YOU`RE DOING, DON`T TOUCH IT
    Composes given image with palette
    Input:
    :param img: a image in numpy array form
    :param RGB_palette: a palette in standard python List[List[int]] format of colors in RGB uint8 format
    Output:
    Will output an image, which will contain given image and palette in numpy array form
    Intended for saving on hard drive via skimage.io.imsave method
    """

    bg_height = round(img.shape[0] * 1.5)
    if img.shape[1] > bg_height:
        bg_height = round(img.shape[1] * 1.5)
    bg_width = bg_height
    bg = full((bg_height, bg_width, 3), 255, dtype='uint8')

    n_img = image(img)
    n_bg = image(bg)

    n_img.translate((round((bg_width - img.shape[1]) / 2), 20))
    n_img_ALPHA = n_img.get_alpha()

    m1 = image.merge(n_bg, n_img, n_img_ALPHA)

    col_interv = 20
    height_interv = img.shape[0] + round(bg_height / 10)
    col_space = (bg_width - col_interv * 2) - (len(RGB_palette) - 1) * col_interv
    if col_space <= 0:
        raise Exception("IMAGE TOO SMALL TO PREVIEW, PLEASE INCREASE THE PIX LIMIT / UPSCALE THE IMAGE")
    cube_side = round(col_space / len(RGB_palette))

    c_cube_MAIN = full((cube_side, cube_side, 3), RGB_palette[0], dtype='uint8')
    n_c_cube_MAIN = image(c_cube_MAIN)
    n_c_cube_MAIN.translate((col_interv, col_interv + height_interv))
    n_c_cube_MAIN_ALPHA = n_c_cube_MAIN.get_alpha()

    pre_comp = image.merge(m1, n_c_cube_MAIN, n_c_cube_MAIN_ALPHA)

    n = 0
    for i in RGB_palette:
        n += 1
        if n == 1:
            continue
        c_cubeN = image(c_cube_MAIN)
        c_cubeN.translate((col_interv, col_interv + height_interv))
        c_cubeN.translate(((col_interv + cube_side) * (n - 1), 0))
        c_cubeN.change_color(i)
        c_cubeN_ALPHA = c_cubeN.get_alpha()
        pre_comp = image.merge(pre_comp, c_cubeN, c_cubeN_ALPHA)

    return image.convert_to_numpy(pre_comp, bg_width)


def output_palette(filepath: str, colors: int = 8, sort_by_lightness: bool = False,
                   pix_limit: int = 200000) -> List[List[int]]:
    """
    Reads an image, reformats it and generates a palette out of it.
    Input:
    :param filepath: a path to the image, which you want to get the palette out of
    :param colors: amount of colors in palette
    :param sort_by_lightness: whether to sort palette by lightness of it`s components or not
    :param pix_limit: a maximum amount of pixels in the formatted image
    Output:
    Will output a standard python list of lists of RGB colors in uint8 format ([[5,5,5],[6,6,6],...] for example)
    """
    img = read_image(filepath)

    try:
        img_height, img_width, chan_amount = img.shape
    except ValueError:
        img_height, img_width = img.shape
        chan_amount = 1

    if not (img_width * img_height <= pix_limit and img.dtype == 'uint8' and chan_amount == 3):
        fmtd_img = _DEV_formatting(img, pix_limit, img_width, img_height, chan_amount, img.dtype)
    else:
        fmtd_img = img

    return palette(fmtd_img, colors=colors, SORT_BY_LIGHTNESS=sort_by_lightness)


def output_image_with_palette(filepath: str, colors: int = 8, sort_by_lightness: bool = False,
                   pix_limit: int = 200000) -> ndarray:
    """
    Reads an image, reformats it, generates a palette out of it and then comps it with the image.
    Input:
    :param filepath: a path to the image, which you want to get the palette out of
    :param colors: amount of colors in palette
    :param sort_by_lightness: whether to sort palette by lightness of it`s components or not
    :param pix_limit: a maximum amount of pixels in the formatted image
    Output:
    Will output an image, which will contain given image and it`s palette in numpy array form
    Intended for saving on hard drive via skimage.io.imsave method
    """
    img = read_image(filepath)

    try:
        img_height, img_width, chan_amount = img.shape
    except ValueError:
        img_height, img_width = img.shape
        chan_amount = 1

    if not (img_width * img_height <= pix_limit and img.dtype == 'uint8' and chan_amount == 3):
        fmtd_img = _DEV_formatting(img, pix_limit, img_width, img_height, chan_amount, img.dtype)
    else:
        fmtd_img = img

    return _DEV_comp_palette_with_picture(fmtd_img, palette(fmtd_img, colors=colors, SORT_BY_LIGHTNESS=sort_by_lightness))


def output_palette_img(filepath: str, colors: int = 8, sort_by_lightness: bool = False,
                   pix_limit: int = 200000) -> List[List[int]]:
    """
    Reads an image, reformats it, generates a palette out of it and then draws it.
    Input:
    :param filepath: a path to the image, which you want to get the palette out of
    :param colors: amount of colors in palette
    :param sort_by_lightness: whether to sort palette by lightness of it`s components or not
    :param pix_limit: a maximum amount of pixels in the formatted image
    Output:
    Will output an picture, which will contain palette of a given image in numpy array form
    Intended for saving on hard drive via skimage.io.imsave method
    """
    img = read_image(filepath)

    try:
        img_height, img_width, chan_amount = img.shape
    except ValueError:
        img_height, img_width = img.shape
        chan_amount = 1

    if not (img_width * img_height <= pix_limit and img.dtype == 'uint8' and chan_amount == 3):
        fmtd_img = _DEV_formatting(img, pix_limit, img_width, img_height, chan_amount, img.dtype)
    else:
        fmtd_img = img

    return _DEV_draw_palette(RGB_pal=palette(fmtd_img, colors=colors, SORT_BY_LIGHTNESS=sort_by_lightness))

