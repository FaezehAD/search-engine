# Generated by Django 4.2.3 on 2023-09-18 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("SE", "0004_remove_journal_pub_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="journalarticle",
            name="vernacular_title",
        ),
    ]
