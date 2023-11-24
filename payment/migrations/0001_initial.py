# Generated by Django 4.2.7 on 2023-11-23 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("order", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("full_name", models.CharField(max_length=150)),
                ("amount", models.PositiveIntegerField()),
                ("ref", models.CharField(max_length=200)),
                ("email", models.EmailField(max_length=254)),
                ("verified", models.BooleanField(default=False)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("phone", models.CharField(max_length=50)),
                ("country", models.CharField(blank=True, max_length=200, null=True)),
                ("state", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "payment_method",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    "order",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="order.order",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-date_created"],
            },
        ),
    ]
