from django.db import models
from donorapp.models import *
from hospitalapp.models import *
from django.utils.timezone import now


# Create your models here.
class Recipient(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="User Name")
    email = models.EmailField(unique=True, verbose_name="Email") 
    password = models.CharField(max_length=128, verbose_name="Password") 
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    address = models.TextField(verbose_name="Address")
    photo = models.ImageField(upload_to='recipient_profiles/', verbose_name="Upload Profile", null=True, blank=True)
    otp = models.CharField(max_length=6, default='000000', verbose_name="OTP", help_text='Enter OTP for verification')
    otp_status = models.CharField(max_length=15, default='Not Verified', verbose_name="OTP Status", help_text='OTP status')

    def __str__(self):
        return self.full_name
    


class OrganRequest(models.Model):
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, verbose_name="Recipient", related_name='organ_requests')
    hospital = models.ForeignKey(
        Hospital, 
        on_delete=models.CASCADE, 
        related_name='organ_requests', 
        verbose_name="Hospital",
        null=True, 
        blank=True, 
    )
    full_name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    organs_needed = models.CharField(max_length=500, verbose_name="Organs Needed") 
    urgency_level = models.CharField(max_length=10, choices=[
        ('high', 'High - Immediate'),
        ('medium', 'Medium - Within 6 months'),
        ('low', 'Low - Routine')
    ], verbose_name="Urgency Level")
    status = models.CharField(max_length=10, choices=[
        ('pending', 'Request Submitted. The recipient is waiting for a donor.'),
        ('matched', 'Donor Found. A suitable donor has been found for the recipient.'),
        ('completed', 'Transplant Successful. The organ transplant was successful.')
    ], default='pending', verbose_name="Status")
    linked_donation = models.ForeignKey(Donation, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Linked Donation")

    def __str__(self):
        return f"{self.full_name} - {self.urgency_level}"
    
    def get_status_display_verbose(self):
        return dict(self._meta.get_field('status').flatchoices).get(self.status, 'Unknown')
    



class OrganTransactionDetail(models.Model):
    organ_request = models.ForeignKey(
        OrganRequest, 
        on_delete=models.CASCADE, 
        related_name="organ_transaction_details"
    )
    hospital = models.ForeignKey(
        Hospital, 
        on_delete=models.SET_NULL,  # Use SET_NULL to not delete the transaction details if the hospital is deleted
        null=True, 
        blank=True, 
        related_name="hospital_transactions"
    )
    transaction_hash = models.CharField(max_length=64)
    sender_address = models.CharField(max_length=42)
    contract_address = models.CharField(max_length=42)
    gas_used = models.BigIntegerField()
    block_number = models.BigIntegerField()
    gas_limit = models.BigIntegerField()  
    mined_on = models.DateTimeField(default=now)  
    block_hash = models.CharField(max_length=64)  
    value = models.BigIntegerField(default=0)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        hospital_name = self.hospital.name if self.hospital else 'Unknown Hospital'
        return f"Transaction {self.transaction_hash} for Request {self.organ_request.id} at {hospital_name}"