from django.db import models


def default_cropmode():
    cropmode = {
        "left_horizontal": [0, 1],
        "right_horizontal": [0, 1],
        "first_vertical": [0, 1],
        "vertical": [0, 1],
        "check_range": [1, 1],
    }

    return cropmode


class ImageCutterOption(models.Model):
    name = models.CharField("Name of option", max_length=64)
    desc = models.TextField("Description of option")

    cropmode = models.JSONField("Crop option data", default=default_cropmode)
