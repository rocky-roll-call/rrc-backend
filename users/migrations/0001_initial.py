# Generated by Django 2.1.7 on 2019-03-17 03:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    sorl.thumbnail.fields.ImageField(
                        blank=True,
                        upload_to=users.models.profile_image,
                        verbose_name="Profile Photo",
                    ),
                ),
                ("full_name", models.CharField(blank=True, max_length=128)),
                (
                    "alt",
                    models.CharField(
                        blank=True, max_length=128, verbose_name="Stage Name"
                    ),
                ),
                (
                    "bio",
                    models.TextField(
                        blank=True, max_length=500, verbose_name="Public Bio"
                    ),
                ),
                ("location", models.CharField(blank=True, max_length=64)),
                (
                    "external_url",
                    models.URLField(blank=True, verbose_name="Personal Website"),
                ),
                (
                    "facebook_url",
                    models.URLField(blank=True, verbose_name="Facebook Page"),
                ),
                (
                    "twitter_user",
                    models.CharField(
                        blank=True, max_length=15, verbose_name="Twitter Username"
                    ),
                ),
                (
                    "instagram_user",
                    models.CharField(
                        blank=True, max_length=30, verbose_name="Instagram Username"
                    ),
                ),
                (
                    "show_email",
                    models.BooleanField(
                        default=False, verbose_name="Show Email on Profile"
                    ),
                ),
                (
                    "searchable",
                    models.BooleanField(
                        default=True, verbose_name="Searchable Profile"
                    ),
                ),
                ("email_confirmed", models.BooleanField(default=False)),
                ("birth_date", models.DateField(blank=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        )
    ]
