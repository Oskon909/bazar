# Generated by Django 4.1 on 2022-09-15 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("oskon", "0022_alter_views_post"),
    ]

    operations = [
        migrations.AddField(
            model_name="phonenumber",
            name="view",
            field=models.IntegerField(default=0),
        ),
    ]
