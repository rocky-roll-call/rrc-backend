# Generated by Django 2.1.7 on 2019-04-07 17:07

from django.db import migrations, models
import sorl.thumbnail.fields
import users.models


class Migration(migrations.Migration):

    dependencies = [("users", "0003_auto_20190402_0149")]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="alt",
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name="profile",
            name="bio",
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name="profile", name="external_url", field=models.URLField(blank=True)
        ),
        migrations.AlterField(
            model_name="profile", name="facebook_url", field=models.URLField(blank=True)
        ),
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=sorl.thumbnail.fields.ImageField(
                blank=True, upload_to=users.models.profile_image
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="instagram_user",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name="profile",
            name="searchable",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="show_email",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="profile",
            name="twitter_user",
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
