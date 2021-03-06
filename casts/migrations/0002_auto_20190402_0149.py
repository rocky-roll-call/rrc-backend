# Generated by Django 2.1.7 on 2019-04-02 01:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [("casts", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="cast",
            name="modified_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="cast",
            name="created_date",
            field=models.DateTimeField(
                default=django.utils.timezone.now, editable=False
            ),
        ),
        migrations.AlterField(
            model_name="castphoto",
            name="created_date",
            field=models.DateTimeField(
                default=django.utils.timezone.now, editable=False
            ),
        ),
        migrations.AlterField(
            model_name="pagesection",
            name="created_date",
            field=models.DateTimeField(
                default=django.utils.timezone.now, editable=False
            ),
        ),
    ]
