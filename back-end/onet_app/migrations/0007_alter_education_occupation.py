# Generated by Django 5.0.4 on 2024-04-13 19:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("onet_app", "0006_remove_education_category_education_description"),
        ("openai_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="education",
            name="occupation",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="education",
                to="openai_app.occupation",
            ),
        ),
    ]