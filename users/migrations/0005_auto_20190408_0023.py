# Generated by Django 2.1.7 on 2019-04-08 00:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("users", "0004_auto_20190407_1707")]

    operations = [
        migrations.RenameField(
            model_name="userphoto", old_name="created_date", new_name="created"
        )
    ]
