from django.shortcuts import render,redirect,get_object_or_404
from donorapp.models import *
from recipientapp.models import *
from hospitalapp.models import *
from django.contrib import messages
import urllib.request
import urllib.parse
from django.contrib.auth import logout
from django.core.mail import send_mail
import os
import random
from django.conf import settings
import json
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
import datetime
# Create your views here.

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')



def sendSMS(user, otp, mobile):
    data = urllib.parse.urlencode(
        {
            "username": "Codebook",
            "apikey": "56dbbdc9cea86b276f6c",
            "mobile": mobile,
            "message": f"Hello {user}, your OTP for account activation is {otp}. This message is generated from https://www.codebook.in server. Thank you",
            "senderid": "CODEBK",
        }
    )
    data = data.encode("utf-8")
    request = urllib.request.Request("https://smslogin.co/v3/api.php?")
    f = urllib.request.urlopen(request, data)
    return f.read()


def generate_otp(length=4):
    otp = "".join(random.choices("0123456789", k=length))
    return otp


def donor_dashboard(request):
    return render(request, "donor/donor-dashboard.html")



from web3 import Web3
from eth_utils import to_checksum_address
import hashlib

# Initialize a web3 instance connected to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Convert the contract address to a checksum address
contract_address = to_checksum_address('0xd8ad04f4f44c331fecf4669a0e9554980823cab3')

# Define your contract's ABI
contract_abi = [
    {
        "constant": False,
        "inputs": [{"name": "_hashValue", "type": "string"}],
        "name": "storeHashValue",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
    # Add more functions from your contract's ABI as needed
]

# Specify the account from which the transaction originates
# Replace 'YOUR_ACCOUNT_ADDRESS' with the address of your account in Ganache
from_account = w3.eth.accounts[0]

# Instantiate your contract object
contract = w3.eth.contract(address=contract_address, abi=contract_abi)


def donor_donation(request):
    if request.method == 'POST':
        print(request.POST)
        donor_id = request.session.get('donor_id_after_login')
        if donor_id:
            try:
                donor = Donor.objects.get(id=donor_id)
                full_name = request.POST.get('donorName')
                age = request.POST.get('donorAge')
                blood_group = request.POST.get('donorBloodGroup')
                address = request.POST.get('donorAddress')
                email = request.POST.get('emailAddress')
                contact_number = request.POST.get('contactNumber')
                selected_organs = request.POST.getlist('selected_organs')
                additional_info = request.POST.get('additionalInfo')
                donation = Donation.objects.create(
                    donor=donor,
                    full_name=full_name,
                    age=age,
                    blood_group=blood_group,
                    address=address,
                    email=email,
                    contact_number=contact_number,
                    organs_to_donate=selected_organs,
                    additional_info=additional_info
                )

                # Generate hash value for donation data
                donation_data = f"{full_name}{age}{blood_group}{address}{email}{contact_number}{','.join(selected_organs)}{additional_info}"
                hash_value = hashlib.sha256(donation_data.encode()).hexdigest()

                # Store hash value in Ganache
                tx_hash = contract.functions.storeHashValue(hash_value).transact({'from': from_account})
                tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

                # Get block details
                block = w3.eth.get_block(tx_receipt.blockNumber)

                # Print all details
                print("Transaction Hash:", tx_receipt.transactionHash.hex())
                print("Sender Address:", tx_receipt['from'])
                print("Contract Address:", tx_receipt.to)
                print("Gas Used:", tx_receipt.gasUsed)
                print("Block Number:", tx_receipt.blockNumber)
                print("Gas Limit:", block.gasLimit)
                print("Block Mined On:", datetime.datetime.utcfromtimestamp(block.timestamp))
                print("Block Hash:", block.hash.hex())
                print("Value in Transaction Receipt:", tx_receipt.get('value', 'Value not found'))
                if 'value' in tx_receipt:
                    value_to_store = tx_receipt['value']
                else:
                    value_to_store = 0
                # Create TransactionDetail object
                transaction_detail = TransactionDetail.objects.create(
                    donation=donation,
                    transaction_hash=tx_receipt.transactionHash.hex(),
                    sender_address=tx_receipt['from'],
                    contract_address=tx_receipt.to,
                    gas_used=tx_receipt.gasUsed,
                    block_number=tx_receipt.blockNumber,
                    gas_limit=block.gasLimit,
                    mined_on=datetime.datetime.utcfromtimestamp(block.timestamp),
                    block_hash=block.hash.hex(),
                    value=value_to_store
                )
                messages.success(request, 'Donation submitted successfully!')
                return redirect('donor_donation')
            except Donor.DoesNotExist:
                messages.error(request, 'Donor does not exist!')
            except Exception as e:
                print(f"Error: {str(e)}")  # Print any other exceptions that occur
                messages.error(request, f'An error occurred: {str(e)}')
    return render(request, "donor/donor-organdonation.html")


def index(request):
    return render(request, "donor/index.html")


def about(request):
    return render(request, "donor/about.html")




def donor_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            donor = Donor.objects.get(email=email)
            if donor.password != password:
                messages.error(request, "Incorrect password.")
                return redirect("donor_login")
            if donor.otp_status == "Verified":
                request.session["donor_id_after_login"] = donor.pk
                messages.success(request, "Login successful!")
                return redirect("donor_dashboard")
            else:
                new_otp = generate_otp()
                donor.otp = new_otp
                donor.otp_status = "Not Verified"
                donor.save()
                subject = "New OTP for Verification"
                message = f"Your new OTP for verification is: {new_otp}"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [donor.email]
                send_mail(
                    subject, message, from_email, recipient_list, fail_silently=False
                )
                sendSMS(donor.full_name, new_otp, donor.phone_number)
                messages.warning(
                    request,
                    "OTP not verified. A new OTP has been sent to your email and phone.",
                )
                request.session["id_for_otp_verification_donor"] = donor.pk
                return redirect("donor_otp")
        except Donor.DoesNotExist:
            messages.error(request, "Email not registered.")
            return redirect("donor_login")
    return render(request, "donor/donor-login.html")




def donor_logout(request):
    logout(request)
    messages.info(request, "Logout Successfully ")
    return redirect("donor_login")




def donor_register(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password') 
        phone_number = request.POST.get('phone_number')
        blood_group = request.POST.get('blood_group')
        address = request.POST.get('address')
        photo = request.FILES.get('photo')
        if Donor.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect('donor_register') 
        donor = Donor(
            full_name=full_name,
            email=email,
            password=password, 
            phone_number=phone_number,
            blood_group=blood_group,
            address=address,
            photo=photo
        )
        otp = generate_otp()
        donor.otp = otp
        donor.save()
        subject = "OTP Verification for Account Activation"
        message = f"Hello {full_name},\n\nYour OTP for account activation is: {otp}\n\nIf you did not request this OTP, please ignore this email."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        request.session["id_for_otp_verification_donor"] = donor.pk
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        if sendSMS:
            sendSMS(full_name, otp, phone_number)
        messages.success(request, "Otp is sent your mail and phonenumber !")
        return redirect("donor_otp")
    return render(request, "donor/donor-register.html")





def donor_otp(request):
    otp_user_id = request.session.get("id_for_otp_verification_donor")
    if not otp_user_id:
        messages.error(request, "No OTP session found. Please try again.")
        return redirect("donor_register")
    if request.method == "POST":
        entered_otp = "".join(
            [
                request.POST["first"],
                request.POST["second"],
                request.POST["third"],
                request.POST["fourth"],
            ]
        )
        try:
            user = Donor.objects.get(id=otp_user_id)
        except Donor.DoesNotExist:
            messages.error(request, "User not found. Please try again.")
            return redirect("donor_register")
        if user.otp == entered_otp:
            user.otp_status = "Verified"
            user.save()
            messages.success(request, "OTP verification successful!")
            return redirect("donor_login")
        else:
            messages.error(request, "Incorrect OTP. Please try again.")
            return redirect("donor_otp")
    return render(request, "donor/donor-otp.html")





def recipient_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            recipient = Recipient.objects.get(email=email)
            if recipient.password != password:
                messages.error(request, "Incorrect password.")
                return redirect("recipient_login")
            if recipient.otp_status == "Verified":
                request.session["recipient_id_after_login"] = recipient.pk
                messages.success(request, "Login successful!")
                return redirect("recipient_dashboard")
            else:
                new_otp = generate_otp()
                recipient.otp = new_otp
                recipient.otp_status = "Not Verified"
                recipient.save()
                subject = "New OTP for Verification"
                message = f"Your new OTP for verification is: {new_otp}"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [recipient.email]
                send_mail(
                    subject, message, from_email, recipient_list, fail_silently=False
                )
                sendSMS(recipient.full_name, new_otp, recipient.phone_number)
                messages.warning(
                    request,
                    "OTP not verified. A new OTP has been sent to your email and phone.",
                )
                request.session["id_for_otp_verification_recipient"] = recipient.pk
                return redirect("recipient_otp")
        except Donor.DoesNotExist:
            messages.error(request, "Email not registered.")
            return redirect("recipient_login")
    return render(request, "donor/recipient-login.html")



def recipient_logout(request):
    logout(request)
    messages.info(request, "Logout Successfully ")
    return redirect("recipient_login")



def recipient_register(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')  
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        photo = request.FILES.get('photo')
        if Recipient.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect('recipient_register')
        recipient = Recipient(
            full_name=full_name,
            email=email,
            password=password,  
            phone_number=phone_number,
            address=address,
            photo=photo,
            otp=generate_otp(),
            otp_status='Not Verified'
        )
        recipient.save()
        subject = "OTP Verification for Account Activation"
        message = f"Hello {full_name},\n\nYour OTP for account activation is: {recipient.otp}\n\nPlease use this OTP to complete your registration."
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, [email], fail_silently=False)
        sendSMS(full_name, recipient.otp, phone_number)
        request.session["id_for_otp_verification_recipient"] = recipient.pk
        messages.success(request, "Registration successful! Please check your email to verify your account.")
        return redirect("recipient_otp") 
    return render(request, "donor/recipient-register.html")



def recipient_otp(request):
    otp_user_id = request.session.get("id_for_otp_verification_recipient")
    if not otp_user_id:
        messages.error(request, "No OTP session found. Please try again.")
        return redirect("recipient_register")
    if request.method == "POST":
        entered_otp = "".join(
            [
                request.POST["first"],
                request.POST["second"],
                request.POST["third"],
                request.POST["fourth"],
            ]
        )
        try:
            user = Recipient.objects.get(pk=otp_user_id)
        except Recipient.DoesNotExist:
            messages.error(request, "User not found. Please try again.")
            return redirect("recipient_register")
        if user.otp == entered_otp:
            user.otp_status = "Verified"
            user.save()
            messages.success(request, "OTP verification successful!")
            return redirect("recipient_login")
        else:
            messages.error(request, "Incorrect OTP. Please try again.")
            return redirect("recipient_otp")
    return render(request, "donor/recipient-otp.html")



def hospital_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            hospital = Hospital.objects.get(email=email)
        except Hospital.DoesNotExist:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('hospital_login') 
        if password == hospital.password:  
            if hospital.status == 'Pending':
                messages.error(request, "Your account is under pending approval. Please come back later or contact admin.")
            elif hospital.status == 'Rejected':
                messages.error(request, "Your hospital's registration is on hold due to some discrepancies. Please contact admin to resolve this.")
            else:
                request.session["id_for_hospital_after_login"] = hospital.pk
                messages.success(request, "Login successful!")
                return redirect('hospital_dashboard') 
        else:
            messages.error(request, "Invalid password. Please try again.")
            return redirect('hospital_login')
    return render(request, "donor/hospital-login.html")



def hospital_logout(request):
    logout(request)
    messages.info(request, "Logout Successfully ")
    return redirect("hospital_login")
from web3 import Web3
from eth_utils import to_checksum_address
import hashlib

# Initialize a web3 instance connected to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Convert the contract address to a checksum address
contract_address = to_checksum_address('0xd8ad04f4f44c331fecf4669a0e9554980823cab3')

# Define your contract's ABI
contract_abi = [
    {
        "constant": False,
        "inputs": [{"name": "_hashValue", "type": "string"}],
        "name": "storeHashValue",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
    # Add more functions from your contract's ABI as needed
]

# Specify the account from which the transaction originates
# Replace 'YOUR_ACCOUNT_ADDRESS' with the address of your account in Ganache
from_account = w3.eth.accounts[0]

# Instantiate your contract object
contract = w3.eth.contract(address=contract_address, abi=contract_abi)


def hospital_register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        address = request.POST.get('address')
        profile_image = request.FILES.get('profile')

        if Hospital.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return render(request, "donor/hospital-register.html")

        # Generate a hash value for the hospital registration data
        registration_data = f"{name}{email}{phone}{address}"
        hash_value = hashlib.sha256(registration_data.encode()).hexdigest()

        # Store the hash value in Ganache
        tx_hash = contract.functions.storeHashValue(hash_value).transact({'from': from_account})

        # Wait for the transaction to be mined
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        block = w3.eth.get_block(tx_receipt.blockNumber)

        # Save the hospital registration data in the database
        new_hospital = Hospital(
            name=name,
            email=email,
            phone=phone,
            password=password, 
            address=address,
            profile_image=profile_image,
            status='Pending'
        )
        new_hospital.save()

        transaction_details = {
            "Transaction successful!": True,
            "Hash": tx_receipt.transactionHash.hex(),
            "Sender Address": getattr(tx_receipt, 'from', ''),
            "To Contract Address": tx_receipt.to,
            "Gas Used": tx_receipt.gasUsed,
            "Block Number": tx_receipt.blockNumber,
            "Gas Limit": block.gasLimit,
            "Mined On": datetime.datetime.utcfromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            "Block Hash": block.hash.hex(),
            "Value": tx_receipt.get('value', 0) 
        }
        
        request.session['transaction_details'] = transaction_details
        messages.success(request, "Hospital registered successfully.")
        return redirect('ganache')
    return render(request, "donor/hospital-register.html")


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        if username == "admin"  and password == "admin":
            messages.success(request, 'Login Successfully.')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, "donor/admin-login.html")


def ganache(request):
    transaction_details = request.session.get('transaction_details', {'error': 'No transaction details found.'})
    context = {'transaction_details': transaction_details}
    return render(request, "donor/ganache.html", context)




def donor_myaccount(request):
    donor_id = request.session.get('donor_id_after_login')
    donor_id = Donor.objects.get(pk=donor_id)
    if donor_id:
        try:
            donations = Donation.objects.filter(donor=donor_id)
            return render(request, "donor/donor-myaccount.html", {'donations': donations})
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, "donor/donor-myaccount.html")
    else:
        messages.error(request, "Please log in to view this page.")
        return redirect('donor_login') 



def view_transaction_details(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    transactions = donation.transactions.all()
    return render(request, 'donor/donor-view-transaction-details.html', {
        'donation': donation,
        'transactions': transactions
    })


def contact(request):
    return render(request, "donor/contact.html")

