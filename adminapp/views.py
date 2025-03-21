from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.core.paginator import Paginator
from hospitalapp.models import *
from donorapp.models import *
from recipientapp.models import *
# Create your views here.
def admin_dashboard(request):
    donor_count = Donor.objects.count()
    recipient_count = Recipient.objects.count()
    hospital_count = Hospital.objects.count()
    return render(request, "admin/admin-dashboard.html", {
        'donor_count': donor_count,
        'recipient_count': recipient_count,
        'hospital_count': hospital_count
    })


def admin_pendninghospitals(request):
    pending_hospitals = Hospital.objects.filter(status='Pending').order_by('name')
    paginator = Paginator(pending_hospitals, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "admin/admin-pendninghospitals.html", {'page_obj': page_obj})



def admin_managehospitals(request):
    hospitals = Hospital.objects.filter(status__in=['Approved', 'Rejected']).order_by('name')
    paginator = Paginator(hospitals, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"admin/admin-managehospitals.html", {'page_obj': page_obj})




def admin_donordetails(request):
    donations = Donation.objects.all() 
    return render(request, "admin/admin-donordetails.html", {'donations': donations})




def admin_transplantdetails(request):
    recipients = OrganRequest.objects.all() 
    return render(request,"admin/admin-transplantdetails.html",{'recipients':recipients})





def hospital_accept(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    hospital.status = 'Approved'
    hospital.save()
    messages.success(request, "Hospital has been approved.")
    return redirect('admin_pendninghospitals')


def hospital_remove(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    hospital.delete()
    messages.success(request, "Hospital has been removed.")
    return redirect('admin_pendninghospitals')



def change_hospital_status(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    if hospital.status == 'Approved':
        hospital.status = 'Rejected'
    else:
        hospital.status = 'Approved'
    hospital.save()
    messages.success(request, f"Status changed to {hospital.status}.")
    return redirect('admin_managehospitals')




def remove_hospital(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    hospital.delete()
    messages.success(request, "Hospital successfully removed.")
    return redirect('admin_managehospitals')