# Generated by Django 1.11.20 on 2019-05-23 15:25
from django.db import migrations, models


def change_http_status(apps, schema_editor):
    Redirect = apps.get_model("redirects", "Redirect")
    Redirect.objects.update(http_status=302)


class Migration(migrations.Migration):
    dependencies = [
        ("redirects", "0002_add_missing_model_change_migrations"),
    ]

    operations = [
        migrations.RunPython(change_http_status),
        migrations.AlterField(
            model_name="redirect",
            name="http_status",
            field=models.SmallIntegerField(
                choices=[
                    (301, "301 - Permanent Redirect"),
                    (302, "302 - Temporary Redirect"),
                ],
                default=302,
                verbose_name="HTTP Status",
            ),
        ),
    ]
