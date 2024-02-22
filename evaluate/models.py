from django.db import models


class Evaluation(models.Model):
    # Meta Field
    user = models.ForeignKey(
        "user.User", verbose_name="작성자", on_delete=models.CASCADE
    )
    date_created = models.DateTimeField("작성일자", auto_now=False, auto_now_add=True)

    # Request Field
    name = models.CharField("모의고사의 이름", max_length=50)
    concept = models.TextField("모의고사의 컨셉")
    pros = models.TextField("모의고사의 좋은 점")
    cons = models.TextField("모의고사의 나쁜 점")
    attack = models.TextField("예상 공격")
    defense = models.TextField("공격에 대한 방어")

    # Evaluation Field
    is_checked = models.BooleanField("확인 여부", default=False)
    is_approved = models.BooleanField("승인 여부", default=False)
