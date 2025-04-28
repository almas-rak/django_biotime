from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class TokenLife(models.Model):
    user_pk = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
    )

    limit_life = models.IntegerField(
        verbose_name="Срок жизни",
        null=False,
        blank=False
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата и время создания"
    )
