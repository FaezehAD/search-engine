# Generated by Django 4.2.3 on 2023-09-21 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SE", "0007_testmodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="testmodel",
            name="test3",
            field=models.CharField(max_length=3, null=True),
        ),
    ]
