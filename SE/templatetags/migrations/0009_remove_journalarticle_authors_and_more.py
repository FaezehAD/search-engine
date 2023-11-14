# Generated by Django 4.2.3 on 2023-09-21 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SE", "0008_testmodel_test3"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="journalarticle",
            name="authors",
        ),
        migrations.RemoveField(
            model_name="journalarticle",
            name="english_keywords",
        ),
        migrations.RemoveField(
            model_name="journalarticle",
            name="persian_keywords",
        ),
        migrations.DeleteModel(
            name="TestModel",
        ),
        migrations.AlterField(
            model_name="journal",
            name="web_url",
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="journalauthor",
            name="email",
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.DeleteModel(
            name="JournalArticle",
        ),
    ]
