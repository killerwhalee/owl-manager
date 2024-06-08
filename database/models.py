from django.db import models

from core.utils import uuid_filepath

import uuid


class Problem(models.Model):
    # Core metadata field
    id = models.UUIDField(
        "Problem id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    owner = models.ForeignKey(
        "user.User",
        verbose_name="Owner of problem",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    last_update = models.DateTimeField("Last update", auto_now=True)

    # Main data field
    data = models.BinaryField("Segment data")
    image = models.ImageField("Preview image", upload_to=uuid_filepath)
    tags = models.JSONField("Problem tags", default=dict, blank=True)
