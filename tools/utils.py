from pdf2image import convert_from_path
from PIL import Image
import os


def segmentalize(
    image: Image.Image,
    check_range: tuple[float, float] = (0, 1),
):
    # Get variables
    width, height = image.size
    check_next, check_empty = map(lambda _: int(_ * width), check_range)
    white_space = int(height * 0.005)

    # Cursor for segmentalizing
    cursor_top, cursor_bot = 0, 0

    # Iterate each row in image
    for pixel_y in range(height):
        # Iterate each pixel in a row
        for pixel_x in range(check_empty):
            # Get pixel value for certain position
            pixel_value = image.getpixel((pixel_x, pixel_y))

            # Check if checked position is on character pixel
            if pixel_value != (255, 255, 255):
                # If current row is the start of next segment,
                # split current segment and save it.
                if pixel_x < check_next and cursor_top < cursor_bot:
                    # Set crop area
                    crop_area = (
                        0,
                        max(cursor_top - white_space, 0),
                        width,
                        cursor_bot + white_space,
                    )

                    yield image.crop(crop_area)

                    # And update top, reset bottom
                    cursor_top, cursor_bot = pixel_y, 0

                else:
                    cursor_bot = pixel_y

                break

    crop_area = (
        0,
        max(cursor_top - white_space, 0),
        width,
        cursor_bot + white_space,
    )

    yield image.crop(crop_area)


def run(file_path: str, crop_option: dict):
    # Catch error or exception while running function
    try:
        segment_num = 1

        image_list = convert_from_path(file_path, dpi=600)
        file_name, _ = os.path.splitext(file_path)

        for page_index, image in enumerate(image_list):
            # TODO: Crop page image regarding crop option
            #
            # Check whether current page is first or not
            if page_index == 0:
                crop_left = crop_option.get()
                crop_right = crop_option.get()
            else:
                crop_left = crop_option.get()
                crop_right = crop_option.get()

            # Segmentalize left side of page
            for image in segmentalize(image.crop(), check_range=(0, 1)):
                image.save(f"{file_name}_{segment_num:2d}.png")
                segment_num += 1

            # Segmentalize right side of page
            for image in segmentalize(image.crop(), check_range=(0, 1)):
                image.save(f"{file_name}_{segment_num:2d}.png")
                segment_num += 1

    # If Exception is caught,
    # print error message and return False(fail)
    except Exception as e:
        print(e)
        return False

    # Return True(success) if all done
    return True
