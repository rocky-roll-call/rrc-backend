# Generated by Django 2.2 on 2019-04-08 02:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_enumfield.db.fields
import events.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("casts", "0004_auto_20190408_0023"),
        ("users", "0005_auto_20190408_0023"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
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
                ("name", models.CharField(max_length=128)),
                ("description", models.TextField()),
                ("venue", models.CharField(max_length=256)),
                ("start", models.DateTimeField()),
                ("created", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "cast",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="casts.Cast",
                    ),
                ),
            ],
            options={"ordering": ["start"]},
        ),
        migrations.CreateModel(
            name="Casting",
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
                    "role",
                    django_enumfield.db.fields.EnumField(
                        default=1, enum=events.models.Role
                    ),
                ),
                ("writein", models.CharField(blank=True, max_length=64)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="castings",
                        to="events.Event",
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="castings",
                        to="users.Profile",
                    ),
                ),
            ],
            options={"ordering": ["role"]},
        ),
    ]
