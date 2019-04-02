# Generated by Django 2.1.7 on 2019-04-02 01:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [("users", "0002_userphoto")]

    operations = [
        migrations.RenameField(
            model_name="profile", old_name="full_name", new_name="name"
        ),
        migrations.AlterField(
            model_name="userphoto",
            name="created_date",
            field=models.DateTimeField(
                default=django.utils.timezone.now, editable=False
            ),
        ),
    ]