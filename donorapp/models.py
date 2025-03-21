from django.db import models
from django.utils import timezone
# Create your models here.
class Donor(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="User Name")
    email = models.EmailField(verbose_name="Email")
    password = models.CharField(max_length=128, verbose_name="Password")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    blood_group = models.CharField(max_length=3, choices=[
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ], verbose_name="Blood Group")
    address = models.TextField(verbose_name="Address")
    photo = models.ImageField(upload_to='profiles/', verbose_name="Upload Profile", null=True, blank=True)
    otp = models.CharField(max_length=6, default='000000', help_text='Enter OTP for verification')
    otp_status = models.CharField(max_length=15, default='Not Verified', help_text='OTP status')

    def __str__(self):
        return self.full_name
    



class Donation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name="donations")
    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    blood_group = models.CharField(max_length=3, choices=[
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ])
    address = models.CharField(max_length=255)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    organs_to_donate = models.JSONField(default=list)
    additional_info = models.TextField(blank=True, null=True)
    hospital_status = models.CharField(max_length=100, default='Pending', null=True, choices=[
        ('Pending', 'Pending - Details Submitted, awaiting initial review'),
        ('Testing', 'Conducted Test - Waiting for results to determine suitability for donation'),
        ('Approved', 'Approved - Confirmed as eligible for donation, coordination for further steps underway'),
        ('Rejected', 'Rejected - Determined not suitable for donation based on medical criteria or test results'),
        ('Completed', 'Completed - Transplant completed successfully')
    ])

    def __str__(self):
        return f"Donation by {self.full_name} ({self.blood_group})"

    def get_hospital_status_display_text(self):
        return dict(self._meta.get_field('hospital_status').flatchoices).get(self.hospital_status)
    




class TransactionDetail(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name="transactions")
    transaction_hash = models.CharField(max_length=64)
    sender_address = models.CharField(max_length=42)
    contract_address = models.CharField(max_length=42)
    gas_used = models.BigIntegerField()
    block_number = models.BigIntegerField()
    gas_limit = models.BigIntegerField()
    mined_on = models.DateTimeField(default=timezone.now)
    block_hash = models.CharField(max_length=64)
    value = models.IntegerField()

    def __str__(self):
        return f"Transaction {self.transaction_hash} for Donation {self.donation.id}"