from django.db import models

# Create your models here.
class Hospital(models.Model):
    name = models.CharField(max_length=255, verbose_name="Hospital Name")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=15, verbose_name="Phone Number")
    password = models.CharField(max_length=128, verbose_name="Password")  
    address = models.TextField(verbose_name="Address")
    profile_image = models.ImageField(upload_to='hospital_images/', verbose_name="Hospital Image", null=True, blank=True)
    status = models.CharField(max_length=10, default='Pending', choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ], verbose_name="Approval Status")

    def __str__(self):
        return self.name