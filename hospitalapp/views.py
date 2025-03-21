from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from hospitalapp.models import *
from donorapp.models import *
from recipientapp.models import *
from django.contrib.auth import logout
from django.core.mail import send_mail
import os
from django.conf import settings
import datetime

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")


# Create your views here.
def hospital_dashboard(request):
    pending_organ_requests_count = OrganRequest.objects.filter(status="pending").count()
    completed_organ_requests_count = OrganRequest.objects.filter(
        status="completed"
    ).count()
    pending_donations_count = Donation.objects.filter(hospital_status="Pending").count()
    completed_donations_count = Donation.objects.filter(
        hospital_status="Approved"
    ).count()
    return render(
        request,
        "hospital/hospital-dashboard.html",
        {
            "pending_organ_requests_count": pending_organ_requests_count,
            "completed_organ_requests_count": completed_organ_requests_count,
            "pending_donations_count": pending_donations_count,
            "completed_donations_count": completed_donations_count,
        },
    )


def hospital_donordetails(request):
    donations = Donation.objects.filter(
        hospital_status__in=["Pending", "Testing"]
    ).order_by("-id")
    return render(
        request, "hospital/hospital-donordetails.html", {"donations": donations}
    )


def hospital_organrequests(request):
    organ_requests = OrganRequest.objects.filter(status="pending").order_by(
        "urgency_level"
    )
    return render(
        request,
        "hospital/hospital-organrequests.html",
        {"organ_requests": organ_requests},
    )


def conduct_test(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    donation.hospital_status = "Testing"
    donation.save()
    subject = "Update on Your Health Checkup"
    message = (
        f"Dear {donation.full_name},\n\n"
        "We have successfully completed all the necessary health checkups for your donation process. "
        "The results will be available within a day. We will keep you updated on the next steps "
        "once the results are out. Thank you for your generous commitment to helping others.\n\n"
        "Best regards,\n"
        "The Donation Team"
    )
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [donation.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    messages.success(request, f"Test conducted for donor {donation.full_name}.")
    return redirect("hospital_donordetails")


def approve_donor(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    donation.hospital_status = "Approved"
    donation.save()
    subject = "Approval Confirmation for Organ Donation"
    message = (
        f"Dear {donation.full_name},\n\n"
        "We are pleased to inform you that you have been approved for organ donation. Your commitment to "
        "helping others through this selfless act is greatly appreciated. We will contact you shortly to "
        "discuss the next steps in the donation process.\n\n"
        "Thank you for your generous spirit and willingness to give a new lease on life to others.\n\n"
        "Best regards,\n"
        "The Donation Team"
    )
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [donation.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    messages.success(request, f"Donor {donation.full_name} approved successfully.")
    return redirect("hospital_donordetails")


def reject_donor(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    donation.hospital_status = "Rejected"
    donation.save()
    subject = "Update on Your Organ Donation Process"
    message = (
        f"Dear {donation.full_name},\n\n"
        "After careful consideration and review of your health checkup results, we regret to inform you "
        "that we are unable to proceed with your donation at this time. This decision is based on ensuring "
        "the safety and suitability of donations for both donors and recipients.\n\n"
        "We deeply appreciate your willingness to help and your spirit of giving. Please do not hesitate "
        "to contact us if you have any questions or if you wish to explore other ways in which you can contribute.\n\n"
        "Thank you for your understanding and your readiness to make a difference.\n\n"
        "Best regards,\n"
        "The Donation Team"
    )
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [donation.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    messages.warning(request, f"Donor {donation.full_name} rejected.")
    return redirect("hospital_donordetails")


from web3 import Web3
from eth_utils import to_checksum_address
import hashlib

# Initialize a web3 instance connected to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Convert the contract address to a checksum address
contract_address = to_checksum_address("0xd8ad04f4f44c331fecf4669a0e9554980823cab3")

# Define your contract's ABI
contract_abi = [
    {
        "constant": False,
        "inputs": [{"name": "_hashValue", "type": "string"}],
        "name": "storeHashValue",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    }
    # Add more functions from your contract's ABI as needed
]

# Specify the account from which the transaction originates
# Replace 'YOUR_ACCOUNT_ADDRESS' with the address of your account in Ganache
from_account = w3.eth.accounts[0]

# Instantiate your contract object
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def match_donor(request, organ_request_id):
    organ_request = OrganRequest.objects.get(pk=organ_request_id)
    organs_needed = organ_request.organs_needed.lower().split(", ")
    matched_donors = Donation.objects.filter(hospital_status="Approved")
    matched_donors = [
        donor
        for donor in matched_donors
        if any(
            organ.lower() in map(str.lower, donor.organs_to_donate)
            for organ in organs_needed
        )
    ]
    return render(
        request,
        "hospital/match-donor.html",
        {"organ_request": organ_request, "matched_donors": matched_donors}
    )


def connect_donor(request, organ_request_id, donor_id):
    organ_request = get_object_or_404(OrganRequest, pk=organ_request_id)
    donation = get_object_or_404(Donation, pk=donor_id)
    donation.hospital_status = "Completed"
    donation.save()

    hospital_id = request.session.get("id_for_hospital_after_login")
    hospital = get_object_or_404(Hospital, pk=hospital_id)

    organ_request.hospital = hospital
    organ_request.status = "completed"
    organ_request.linked_donation = donation
    organ_request.save()

    registration_data = f"{donation.full_name}{donation.email}{donation.contact_number}{donation.address}"
    hash_value = hashlib.sha256(registration_data.encode()).hexdigest()
    tx_hash = contract.functions.storeHashValue(hash_value).transact({"from": from_account})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    block = w3.eth.get_block(tx_receipt.blockNumber)

    # Create OrganTransactionDetail object including all details
    organ_transaction_detail = OrganTransactionDetail.objects.create(
        organ_request=organ_request,
        hospital=hospital,
        transaction_hash=tx_receipt.transactionHash.hex(),
        sender_address=tx_receipt['from'],
        contract_address=tx_receipt.to,
        gas_used=tx_receipt.gasUsed,
        block_number=tx_receipt.blockNumber,
        gas_limit=block.gasLimit,
        mined_on=datetime.datetime.utcfromtimestamp(block.timestamp),
        block_hash=block.hash.hex(),
        value=tx_receipt.get('value', 0) 
    )

    transaction_details_connect_donor = (
        f"Transaction successful!\n"
        f"Hash: {organ_transaction_detail.transaction_hash}\n"
        f"Sender Address: {organ_transaction_detail.sender_address}\n"
        f"To Contract Address: {organ_transaction_detail.contract_address}\n"
        f"Gas Used: {organ_transaction_detail.gas_used}\n"
        f"Mined in Block: {organ_transaction_detail.block_number}\n"
        f"Gas Limit: {organ_transaction_detail.gas_limit}\n"
        f"Mined On: {organ_transaction_detail.mined_on}\n"
        f"Block Hash: {organ_transaction_detail.block_hash}\n"
        f"Value: {organ_transaction_detail.value}\n"
    )
    request.session['transaction_details_connect_donor'] = transaction_details_connect_donor

    # Sending email notification to the recipient
    subject = "Your Organ Transplant is Confirmed"
    message = (
        f"Dear {organ_request.full_name},\n\n"
        "We are pleased to inform you that your organ transplant has been successfully arranged. "
        "Please contact us for further details about the procedure and preparations.\n\n"
        "Best regards,\n"
        "The Hospital Team\n\n"
        f"{transaction_details_connect_donor}"
    )
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [organ_request.email]
    send_mail(subject, message, email_from, recipient_list)

    messages.success(
        request,
        f"The donor has been successfully connected, and the recipient has been notified."
    )
    return redirect("match_donor", organ_request_id=organ_request_id)




def hospital_transaction_deatils(request):
    hospital_id = request.session.get("id_for_hospital_after_login")
    organ_requests = OrganRequest.objects.filter(hospital_id=hospital_id)
    return render(request, "hospital/hospital-transaction-deatils.html", {'organ_requests': organ_requests})


def view_transaction_details(request, request_id):
    organ_request = get_object_or_404(OrganRequest, pk=request_id)
    transaction_details = OrganTransactionDetail.objects.filter(organ_request=organ_request)
    return render(request, 'hospital/final.html', {
        'organ_request': organ_request,
        'transaction_details': transaction_details
    })