# Generated by Django 5.0.4 on 2024-04-13 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("onet_app", "0005_alter_knowledge_description"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="education",
            name="category",
        ),
        migrations.AddField(
            model_name="education",
            name="description",
            field=models.JSONField(default=dict),
        ),
    ]
