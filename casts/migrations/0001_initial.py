# Generated by Django 2.1.7 on 2019-03-19 20:31

import casts.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [("users", "0002_userphoto")]

    operations = [
        migrations.CreateModel(
            name="Cast",
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
                    "name",
                    models.CharField(
                        max_length=128, unique=True, verbose_name="Cast Name"
                    ),
                ),
                ("slug", models.SlugField(blank=True, max_length=200, unique=True)),
                ("description", models.TextField(verbose_name="About Us")),
                (
                    "logo",
                    sorl.thumbnail.fields.ImageField(
                        blank=True,
                        upload_to=casts.models.cast_logo,
                        verbose_name="Cast Logo",
                    ),
                ),
                (
                    "email",
                    models.EmailField(max_length=128, verbose_name="Contact Email"),
                ),
                (
                    "created_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "external_url",
                    models.URLField(blank=True, verbose_name="Existing Homepage"),
                ),
                (
                    "facebook_url",
                    models.URLField(blank=True, verbose_name="Facebook Group URL"),
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
                    "blocked",
                    models.ManyToManyField(
                        related_name="blocked_casts", to="users.Profile"
                    ),
                ),
                (
                    "managers",
                    models.ManyToManyField(
                        related_name="managed_casts", to="users.Profile"
                    ),
                ),
                (
                    "member_requests",
                    models.ManyToManyField(
                        related_name="requested_casts", to="users.Profile"
                    ),
                ),
                (
                    "members",
                    models.ManyToManyField(
                        related_name="member_casts", to="users.Profile"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CastPhoto",
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
                    sorl.thumbnail.fields.ImageField(upload_to=casts.models.cast_photo),
                ),
                ("description", models.TextField(blank=True)),
                (
                    "created_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "cast",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="photos",
                        to="casts.Cast",
                    ),
                ),
            ],
            options={"ordering": ["-pk"]},
        ),
        migrations.CreateModel(
            name="PageSection",
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
                    "title",
                    models.CharField(max_length=128, verbose_name="Section Title"),
                ),
                ("text", models.TextField(verbose_name="Content")),
                (
                    "order",
                    models.PositiveSmallIntegerField(
                        default=1, verbose_name="Section Priority"
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "cast",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="page_sections",
                        to="casts.Cast",
                    ),
                ),
            ],
            options={"ordering": ["order"]},
        ),
    ]
