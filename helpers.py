from argparse import ArgumentParser
from typing import Tuple, List
from numpy import ndarray


def get_input_settings() -> Tuple[str, str, bool]:
    parser = ArgumentParser()

    parser.add_argument("--folder")
    parser.add_argument("--layout")
    parser.add_argument("--plate_text", default=False)

    args = parser.parse_args()

    return args.folder, args.layout, args.plate_text


def get_img_height_width(cv_img: ndarray) -> Tuple[int, int]:
    """
    Dump the redundant third argument channels
    """
    return cv_img.shape[:2]


def get_pic_short_filename(pic_full_filename: str) -> str:
    """
    Example:
    https://dbrain-public.s3.amazonaws.com/project/P45/57e647bc-f3ce-4d83-8f9f-fbb00c3e9e7d/fb8e0cc1-317f-4932-9b67-c51d9a8456b8/141.jpg
    ->>
    141.jpg
    """
    return pic_full_filename.split('/')[-1]


def get_pic_folder(pic_filename: str) -> str:
    """
    Example:
    141.jpg
    ->>
    141
    """
    return pic_filename.split('.')[0]


def rel_coords_to_abs(rel_coords: list, pic_width: float, pic_height: float) -> list:
    """
    Given relative coordinates turn them into absolute by multiplying on width & height
    Example:
    [[0.18602540834845735, 0.6778846153846154], [0.26406533575317603, 0.6778846153846154],
    [0.26406533575317603, 0.7548076923076923], [0.18602540834845735, 0.7548076923076923],
    [0.18602540834845735, 0.6778846153846154]]
    multiply by 551(width) and 312(height)
    ->>
    [[102, 211], [145, 211], [145, 235], [102, 235], [102, 211]]

    """
    return [[int(relative_coord[0] * pic_width), int(relative_coord[1] * pic_height)] for relative_coord in rel_coords]


def crop_plate(cv_img: ndarray, top_left_coord: List[int, int], bottom_right_coord: List[int, int]) -> ndarray:
    """
    Given open cv image return cropped image of car plate
    """
    return cv_img[top_left_coord[1]:bottom_right_coord[1], top_left_coord[0]:bottom_right_coord[0]]
