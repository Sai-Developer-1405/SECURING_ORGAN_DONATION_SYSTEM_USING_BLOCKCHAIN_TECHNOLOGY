"""
URL configuration for organdonationproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from django.conf.urls.static import static
from django.conf import settings


from donorapp import views as donorviews
from adminapp import views as adminviews
from hospitalapp import views as hospitalviews
from recipientapp import views as recipientviews

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',donorviews.index,name="index"),
    path('about/',donorviews.about,name="about"),
    path('contact/',donorviews.contact,name="contact"),
    path('donor/login/',donorviews.donor_login,name="donor_login"),
    path('donor/logout/',donorviews.donor_logout,name="donor_logout"),
    path('donor/register/',donorviews.donor_register,name="donor_register"),
    path('donor/otp/',donorviews.donor_otp,name="donor_otp"),
    path('recipient/login/',donorviews.recipient_login,name="recipient_login"),
    path('recipient/logout/',donorviews.recipient_logout,name="recipient_logout"),
    path('recipient/register/',donorviews.recipient_register,name="recipient_register"),
    path('recipient/otp/',donorviews.recipient_otp,name="recipient_otp"),
    path('hospital/login/',donorviews.hospital_login,name="hospital_login"),
    path('hospital/logout/',donorviews.hospital_logout,name="hospital_logout"),
    path('hospital/register/',donorviews.hospital_register,name="hospital_register"),
    path('admin-login/',donorviews.admin_login,name="admin_login"),
    path('ganache/details/',donorviews.ganache,name="ganache"),
    path('donor/ganache/details/',donorviews.donor_myaccount,name="donor_myaccount"),
    path('donation/transaction/<int:donation_id>/', donorviews.view_transaction_details, name='view_transaction_details'),



    path('donor/dashboard/',donorviews.donor_dashboard,name="donor_dashboard"),
    path('donor/organ/donation/',donorviews.donor_donation,name="donor_donation"),





    # Adminurls 

    path('admin-dashboard/',adminviews.admin_dashboard,name="admin_dashboard"),
    path('admin-pending-hospitals/',adminviews.admin_pendninghospitals,name="admin_pendninghospitals"),
    path('admin-manage-hospitals/',adminviews.admin_managehospitals,name="admin_managehospitals"),
    path('admin-donor-details/',adminviews.admin_donordetails,name="admin_donordetails"),
    path('admin-transplant-details/',adminviews.admin_transplantdetails,name="admin_transplantdetails"),
    path('hospital/accept/<int:hospital_id>/', adminviews.hospital_accept, name='hospital_accept'),
    path('hospital/remove/<int:hospital_id>/', adminviews.hospital_remove, name='hospital_remove'),
    path('hospital/change-status/<int:hospital_id>/', adminviews.change_hospital_status, name='change_hospital_status'),
    path('hospital/remove/<int:hospital_id>/', adminviews.remove_hospital, name='remove_hospital'),



    #### recipient views
    path('recipient/dashboard/',recipientviews.recipient_dashboard,name="recipient_dashboard"),
    path('recipient/recipient/form/',recipientviews.recipient_form,name="recipient_form"),
    path('recipient/status/',recipientviews.recipient_status,name="recipient_status"),





    #### hospital View
    path('hospital/dashboard/',hospitalviews.hospital_dashboard,name="hospital_dashboard"),
    path('hospital/donor/details/',hospitalviews.hospital_donordetails,name="hospital_donordetails"),
    path('hospital/organ/requests/',hospitalviews.hospital_organrequests,name="hospital_organrequests"),
    path('donation/test/<int:donation_id>/', hospitalviews.conduct_test, name='conduct_test'),
    path('donation/approve/<int:donation_id>/', hospitalviews.approve_donor, name='approve_donor'),
    path('donation/reject/<int:donation_id>/', hospitalviews.reject_donor, name='reject_donor'),
    path('hospital/matchdonor/<int:organ_request_id>/', hospitalviews.match_donor, name='match_donor'),
    path('connect-donor/<int:organ_request_id>/<int:donor_id>/', hospitalviews.connect_donor, name='connect_donor'),
    path('hospital/ganache/', hospitalviews.hospital_transaction_deatils, name='hospital_transaction_deatils'),
    path('transaction-details/<int:request_id>/', hospitalviews.view_transaction_details, name='view_transaction_details'),
   




]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
