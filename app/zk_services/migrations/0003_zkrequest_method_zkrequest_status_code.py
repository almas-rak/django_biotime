# Generated by Django 4.2.16 on 2024-10-12 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zk_services', '0002_zktoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='zkrequest',
            name='method',
            field=models.CharField(default='GET', verbose_name='Метод'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='zkrequest',
            name='status_code',
            field=models.IntegerField(default=200, verbose_name='Статус код'),
            preserve_default=False,
        ),
    ]
