from django.db import models


class ImageCutterOption(models.Model):
    name = models.CharField("형식 이름", max_length=50)
    data = models.JSONField("형식 데이터")