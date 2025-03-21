# Generated by Django 5.0.5 on 2024-05-09 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donorapp", "0003_donation"),
    ]

    operations = [
        migrations.AddField(
            model_name="donation",
            name="hospital_status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending - Details Submitted, awaiting initial review"),
                    (
                        "Testing",
                        "Conducted Test - Waiting for results to determine suitability for donation",
                    ),
                    (
                        "Approved",
                        "Approved - Confirmed as eligible for donation, coordination for further steps underway",
                    ),
                    (
                        "Rejected",
                        "Rejected - Determined not suitable for donation based on medical criteria or test results",
                    ),
                ],
                default="Pending",
                max_length=100,
                null=True,
            ),
        ),
    ]
