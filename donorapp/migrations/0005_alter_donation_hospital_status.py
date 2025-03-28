# Generated by Django 5.0.5 on 2024-05-10 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donorapp", "0004_donation_hospital_status"),
    ]

    operations = [
        migrations.AlterField(
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
                    ("Completed", "Completed - Transplant completed successfully"),
                ],
                default="Pending",
                max_length=100,
                null=True,
            ),
        ),
    ]
