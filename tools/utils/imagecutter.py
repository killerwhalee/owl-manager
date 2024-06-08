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
    margin = int(0.01 * height)

    # Cursor and flag for segmentalizing
    cursor = 0
    flag = False

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
                if pixel_x < check_next:
                    if not flag:
                        if cursor > 0:
                            crop_area = (
                                0,
                                max(cursor - margin, 0),
                                width,
                                min(pixel_y - margin, height),
                            )

                            yield image.crop(crop_area)

                        cursor = pixel_y
                        flag = True

                else:
                    flag = False

                break

    crop_area = (
        0,
        max(cursor - margin, 0),
        width,
        min(pixel_y + margin, height),
    )

    yield image.crop(crop_area)


def trim_bottom(image: Image.Image, credibility: float = 0.5):
    width, height = image.size

    for pixel_y in range(height - 1, 0, -1):
        for pixel_x in range(int(width * credibility)):
            # Get pixel value for certain position
            pixel_value = image.getpixel((pixel_x, pixel_y))

            if pixel_value != (255, 255, 255):
                crop_area = (0, 0, width, min(pixel_y + 30, height))

                return image.crop(crop_area)


def run(file_path: str, crop_option: dict):
    file_name, _ = os.path.splitext(os.path.basename(file_path))
    segment_num = 1

    print(f"converting {file_name}...")
    image_list = convert_from_path(file_path, dpi=600)

    for page_index, image in enumerate(image_list):
        if page_index == 0:
            t, b = crop_option.get("first_vertical", (0, 1))
        else:
            t, b = crop_option.get("vertical", (0, 1))

        ll, lr = crop_option.get("left_horizontal", (0, 1))
        rl, rr = crop_option.get("right_horizontal", (0, 1))

        w, h = image.size
        l, r = crop_option.get("check_range")

        # Calculate crop area
        ll, lt, lr, lb = ll * w - 10, t * h, lr * w + 30, b * h
        rl, rt, rr, rb = rl * w - 10, t * h, rr * w + 30, b * h

        # Segmentalize left side of page
        for image_seg in segmentalize(image.crop((ll, lt, lr, lb)), check_range=(l, r)):
            image_seg = trim_bottom(image_seg)
            image_seg.save(f"images/{file_name}_{segment_num:02d}.png")
            segment_num += 1

        # Segmentalize right side of page
        for image_seg in segmentalize(image.crop((rl, rt, rr, rb)), check_range=(l, r)):
            image_seg = trim_bottom(image_seg)
            image_seg.save(f"images/{file_name}_{segment_num:02d}.png")
            segment_num += 1


def sample(file_path: str):
    print("converting...")
    image_list = convert_from_path(file_path, dpi=600)

    file_name, _ = os.path.splitext(os.path.basename(file_path))

    for index, image in enumerate(image_list):
        image.save(f"images/{file_name}_{index+1:02d}.png")


cropmode = {
    "left_horizontal": [0.104, 0.482],
    "right_horizontal": [0.518, 0.896],
    "first_vertical": [0.208, 0.909],
    "vertical": [0.125, 0.909],
    "check_range": [0.036, 0.107],
}
