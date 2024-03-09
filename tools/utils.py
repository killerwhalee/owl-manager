from tools.models import ImageCutterOption

from pdf2image import convert_from_path as pdf
from PIL import Image

import os


def run(file_source, file_type):
    success, fail = (0, 0)

    # Load cropMode from cropData JSON file
    image_cutter_option = ImageCutterOption.objects.get(file_type=file_type)
    crop_data = image_cutter_option.data

    leftFirstImageCropPercentage = crop_data[file_type]["leftFirstImageCropPercentage"]
    rightFirstImageCropPercentage = crop_data[file_type][
        "rightFirstImageCropPercentage"
    ]

    leftImageCropPercentage = crop_data[file_type]["leftImageCropPercentage"]
    rightImageCropPercentage = crop_data[file_type]["rightImageCropPercentage"]

    cropCheckRange = crop_data[file_type]["cropCheckRange"]

    # Catch error/exception occur while running function
    try:
        pageNum = 1
        startNum = 1
        pdfFile = pdf(file_source, dpi=600)
        fileName, fileExt = os.path.splitext(file_source)

        for pdfImage in pdfFile:
            pdfImage.save(f"{fileName}-PAGE#{pageNum}-L.png")
            pdfImage.save(f"{fileName}-PAGE#{pageNum}-R.png")
            # pageNum += 1; continue # For raw extraction

            # Typically first page has different form (case specific).
            # If not, FirstImageCropPercentage would be same with
            # ImageCropPercentage in JSON file
            if pageNum % 4 == 1 and (
                leftFirstImageCropPercentage or rightFirstImageCropPercentage
            ):
                leftCropRange = leftFirstImageCropPercentage
                rightCropRange = rightFirstImageCropPercentage
            else:
                leftCropRange = leftImageCropPercentage
                rightCropRange = rightImageCropPercentage

            # This is for Binary Cropping
            if leftCropRange:
                startNum += imgBinaryCrop(
                    f"{fileName}-PAGE#{pageNum}-L.png",
                    dest=fileName,
                    cropRange=leftCropRange,
                    cropCheckRange=cropCheckRange,
                    startNum=startNum,
                    numDigit=2,
                )

            if rightCropRange:
                startNum += imgBinaryCrop(
                    f"{fileName}-PAGE#{pageNum}-R.png",
                    dest=fileName,
                    cropRange=rightCropRange,
                    cropCheckRange=cropCheckRange,
                    startNum=startNum,
                    numDigit=2,
                )

            # This is for Raw Cropping
            # startNum += imgRawCrop(
            #     f"{fileName}-PAGE#{pageNum}-L.png",
            #     dest=f"{fileName}-halfcrop",
            #     cropRange=leftCropRange,
            #     startNum=startNum,
            #     numDigit=2,
            # )
            # startNum += imgRawCrop(
            #     f"{fileName}-PAGE#{pageNum}-R.png",
            #     dest=f"{fileName}-halfcrop",
            #     cropRange=rightCropRange,
            #     startNum=startNum,
            #     numDigit=2,
            # )

            # Remove temporal file created
            os.remove(f"{fileName}-PAGE#{pageNum}-L.png")
            os.remove(f"{fileName}-PAGE#{pageNum}-R.png")

            pageNum += 1

    # We caught some error/exception here.
    # Print error message and exit
    except Exception as e:
        print(f"Error in source [{file_source}] - {e}")
        return False

    return True


def imgBottomTrim(image, whiteSpace):
    # Image Bottom Trimming
    bottomLine = 0
    width, height = image.size

    for heightPixel in range(height):
        for widthPixel in range(int(width * 0.5)):
            if image.getpixel((widthPixel, heightPixel)) != (255, 255, 255):
                bottomLine = heightPixel
                break

    recroppedRegion = 0, 0, width, min(bottomLine + 2 * whiteSpace, height)
    image = image.crop(recroppedRegion)
    return image


def imgRawCrop(src, dest=None, cropRange=(0, 0, 1, 1), startNum=1, numDigit=0):
    if not dest:
        dest = os.path.splitext(src)[0]
    else:
        dest = os.path.splitext(dest)[0]

    image = Image.open(src)
    width, height = image.size
    imageCount = 0

    ## Crop Image
    imageCropArea = (
        int(cropRange[0] * width),
        int(cropRange[1] * height),
        int(cropRange[2] * width),
        int(cropRange[3] * height),
    )
    croppedImage = image.crop(imageCropArea)

    imageStr = str(startNum + imageCount)
    if numDigit:
        imageStr = "0" * (numDigit - len(str(startNum + imageCount))) + str(
            startNum + imageCount
        )

    croppedImage.save(f"{dest}_{imageStr}.png")

    return 1


def imgBinaryCrop(
    src,
    dest=None,
    cropRange=(0, 0, 1, 1),
    cropCheckRange=(0, 0),
    startNum=1,
    numDigit=0,
):

    if not dest:
        dest = os.path.splitext(src)[0]
    else:
        dest = os.path.splitext(dest)[0]

    image = Image.open(src)
    width, height = image.size

    ## Crop Image
    imageCropArea = (
        int(cropRange[0] * width),
        int(cropRange[1] * height),
        int(cropRange[2] * width),
        int(cropRange[3] * height),
    )
    croppedImage = image.crop(imageCropArea)
    width, height = croppedImage.size
    whiteSpace = int(height * 0.005)

    ## Variable Set
    imageCount = 0
    boundRange = [0, 0]

    # Cut Each Paragraph in Cropped Page
    for heightPixel in range(height):
        for widthPixel in range(int(width * cropCheckRange[1])):
            if croppedImage.getpixel((widthPixel, heightPixel)) != (255, 255, 255):
                if widthPixel < width * cropCheckRange[0]:
                    if boundRange[1]:
                        recroppedRegion = (
                            0,
                            max(boundRange[0] - whiteSpace, 0),
                            width,
                            heightPixel - whiteSpace,
                        )
                        croppedHeight = (heightPixel - 1) - max(
                            boundRange[0] - whiteSpace, 0
                        )

                        if boundRange[0]:
                            imageStr = str(startNum + imageCount)
                            if numDigit:
                                imageStr = "0" * (
                                    numDigit - len(str(startNum + imageCount))
                                ) + str(startNum + imageCount)

                            unTrimmedImage = croppedImage.crop(recroppedRegion)
                            outputImage = imgBottomTrim(unTrimmedImage, whiteSpace)
                            outputImage.save(f"{dest}_{imageStr}.png")

                            imageCount += 1

                        boundRange = [0, 0]

                    if not boundRange[0]:
                        boundRange[0] = heightPixel

                else:
                    boundRange[1] = heightPixel

                break

    recroppedRegion = (
        0,
        max(boundRange[0] - whiteSpace, 0),
        width,
        heightPixel - whiteSpace,
    )
    croppedHeight = (heightPixel - 1) - max(boundRange[0] - whiteSpace, 0)

    if boundRange[0]:
        imageStr = str(startNum + imageCount)
        imageStr = "0" * (numDigit - len(str(startNum + imageCount))) + str(
            startNum + imageCount
        )

        unTrimmedImage = croppedImage.crop(recroppedRegion)
        outputImage = imgBottomTrim(unTrimmedImage, whiteSpace)
        outputImage.save(f"{dest}_{imageStr}.png")

        imageCount += 1

    return imageCount
