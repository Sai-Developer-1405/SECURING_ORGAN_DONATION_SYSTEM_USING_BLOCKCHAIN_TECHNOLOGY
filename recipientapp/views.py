from django.shortcuts import render,redirect,get_object_or_404
from donorapp.models import *
from recipientapp.models import *
from django.contrib import messages
# Create your views here.
def recipient_dashboard(request):
    return render(request,"recipient/recipient-dashboard.html")


def recipient_form(request):
    if request.method == "POST":
        # id = request.session.get("id_for_hospital_after_login")
        # hospital = Hospital.objects.get(pk=id)
        recipient_id = request.session.get('recipient_id_after_login')
        if not recipient_id:
            messages.error(request, "You must be logged in to submit a request.")
            return redirect('recipient_login')  
        try:
            recipient = Recipient.objects.get(id=recipient_id)
        except Recipient.DoesNotExist:
            messages.error(request, "Recipient not found.")
            return redirect('recipient_login') 
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        organs_needed = ', '.join(request.POST.getlist('organ_needed'))  
        urgency_level = request.POST.get('urgency_level')
        organ_request = OrganRequest(
            recipient=recipient,
            # hospital = hospital,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            organs_needed=organs_needed,
            urgency_level=urgency_level
        )
        organ_request.save()
        messages.success(request, "Your organ request has been submitted successfully.")
        return redirect('recipient_form') 
    return render(request, "recipient/recipient-form.html")




def recipient_status(request):
    recipient_id = request.session.get('recipient_id_after_login')
    recipient = get_object_or_404(Recipient, id=recipient_id)
    organ_requests = OrganRequest.objects.filter(recipient=recipient)
    return render(request, "recipient/status.html", {'organ_requests': organ_requests})