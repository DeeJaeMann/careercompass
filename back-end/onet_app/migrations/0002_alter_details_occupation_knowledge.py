# Generated by Django 5.0.4 on 2024-04-11 20:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("onet_app", "0001_initial"),
        ("openai_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="details",
            name="occupation",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="details",
                to="openai_app.occupation",
            ),
        ),
        migrations.CreateModel(
            name="Knowledge",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category", models.CharField(max_length=150)),
                ("description", models.CharField(max_length=150)),
                (
                    "occupation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="knowledge",
                        to="openai_app.occupation",
                    ),
                ),
            ],
        ),
    ]
