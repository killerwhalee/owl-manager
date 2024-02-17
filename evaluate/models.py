from django.db import models


class Evaluation(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    