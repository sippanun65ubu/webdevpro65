# Generated by Django 5.1.1 on 2024-09-30 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("promanagement", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name="post",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
