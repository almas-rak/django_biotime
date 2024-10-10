from django.contrib.auth import get_user_model
from django.db import models

from zk_services.token_manager import TokenManager


# Create your models here.
class ZkRequest(models.Model):
    user_pk = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
    )
    request = models.CharField(
        verbose_name="Запрос",
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время создания"
    )


class ZkToken(models.Model):
    token = models.CharField(
        verbose_name="Токен",
        null=False,
        blank=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время создания"
    )

    objects = TokenManager()
