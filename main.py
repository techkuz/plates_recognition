import json
import cv2 as cv
import pytesseract
import pathlib

from helpers import (get_input_settings, get_pic_short_filename, get_pic_folder,
                     get_img_height_width, rel_coords_to_abs, crop_plate)

config = {'pytesseract_config': '-l eng --oem 1 --psm 7',
          'output_folder': 'labeled'}

if __name__ == "__main__":
    pictures_folder, layout_file, plate_to_text = get_input_settings()
    output_folder = config['output_folder']

    with open(file=layout_file) as lf:
        file_json = json.load(lf)
        data = file_json['data']

        for picture in data:
            pic_full_filename = picture['input']['image']
            pic_short_filename = get_pic_short_filename(pic_full_filename=pic_full_filename)
            pic_folder = output_folder + '/' + get_pic_folder(pic_filename=pic_short_filename)

            payload = picture.get('payload', None)
            if payload:
                relative_coords = payload.get('aabb', None).get('license_plate', None)
                picture_path = pictures_folder + '/' + pic_short_filename
                img = cv.imread(picture_path)
                height, width = get_img_height_width(cv_img=img)

                pathlib.Path(pic_folder).mkdir(parents=True, exist_ok=True)

                for index, relative_coords_list in enumerate(relative_coords, start=1):
                    abs_coordinates = rel_coords_to_abs(rel_coords=relative_coords_list,
                                                        pic_width=width, pic_height=height)
                    top_left_coord = abs_coordinates[0]
                    bottom_right_coord = abs_coordinates[2]
                    cropped_plate = crop_plate(cv_img=img, bottom_right_coord=bottom_right_coord,
                                               top_left_coord=top_left_coord)

                    cropped_plate_filename = pic_folder + '/' + str(index)
                    cropped_plate_filename_jpg = cropped_plate_filename + '.jpg'
                    cv.imwrite(cropped_plate_filename_jpg, cropped_plate)

                    #  experimental
                    #  TODO: add pre-processing for better ocr results
                    if plate_to_text:
                        text = pytesseract.image_to_string(cropped_plate,
                                                           config=config['pytesseract_config'])
                        cropped_plate_filename_text = cropped_plate_filename + '.txt'
                        with open(file=cropped_plate_filename_text, mode="w+") as text_file:
                            text_file.write(text if text else "Plate is not recognized")
