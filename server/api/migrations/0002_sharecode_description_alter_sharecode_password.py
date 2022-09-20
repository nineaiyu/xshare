# Generated by Django 4.1.1 on 2022-09-19 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="sharecode",
            name="description",
            field=models.CharField(blank=True, max_length=256, verbose_name="备注信息"),
        ),
        migrations.AlterField(
            model_name="sharecode",
            name="password",
            field=models.CharField(
                blank=True, max_length=16, null=True, verbose_name="访问密码"
            ),
        ),
    ]
