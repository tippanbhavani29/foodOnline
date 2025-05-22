from imaplib import _Authenticator
from pyexpat.errors import messages
from django.contrib import auth
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.forms import UserForm
from accounts.models import User, UserProfile
from accounts.utils import detectuser, send_verification_email
from vendor.forms import VendorForm
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
def check_role_vendor(user):
   if user.role == 1:
       return True
   else: 
      raise PermissionDenied
def check_role_customer(user):
   if user.role == 2:
       return True
   else: 
      raise PermissionDenied
   
def register_user(request):
    if request.method=='POST':
        #store data 
        # print(request.POST)
        form=UserForm(request.POST)
        if form.is_valid():
        #    user=form.save(commit=False)
        #    user.role=User.CUSTOMER
        #    user.save()
           first_name=form.cleaned_data['first_name']
           last_name=form.cleaned_data['last_name']
           username=form.cleaned_data['username']
           email=form.cleaned_data['email']
           password=form.cleaned_data['password']
           user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password)

           user.role=User.CUSROMER
           user.save()
           mail_subject='please activate your account'
           email_template='accounts/email/account_verfication_emil.html'

           send_verification_email(request,user,mail_subject,email_template)
           messages.error(request,"succesfuly registerd as customer")
           return redirect('registerUser') 
        else:
           print("invalid form")
           print(form.errors)
    else:
     form=UserForm()
    context={
        'form':form,
    }
    return  render(request,"accounts/registerUser.html",context)
# Create your views here.
def register_ven(request):
    if request.method=='POST':
        #store data 
        # print(request.POST)
        form=UserForm(request.POST)
        v_form=VendorForm(request.POST,request.FILES)
        if form.is_valid():
        #    user=form.save(commit=False)
        #    user.role=User.CUSTOMER
        #    user.save()
           first_name=form.cleaned_data['first_name']
           last_name=form.cleaned_data['last_name']
           username=form.cleaned_data['username']
           email=form.cleaned_data['email']
           password=form.cleaned_data['password']
           user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)

           user.role=User.RESTAURANT
           user.save()
           vendor=v_form.save(commit=False)
           vendor.user=user
           user_profile=UserProfile.objects.get(user=user)
           vendor.user_profile=user_profile
           vendor.save()
           mail_subject='please activate your account'
           email_template='accounts/email/account_verfication_emil.html'

           send_verification_email(request,user,mail_subject,email_template)
           messages.error(request,"succesfully registere!! Please Wait for the approval")
           return redirect('registerVendor') 
        else:
           print("invalid form")
           print(form.errors)
    else:
     form=UserForm()
     v_form=VendorForm()
    context={
        'form':form,
        'v_form':v_form
    }
    return  render(request,"accounts/registerVendor.html",context)
def login(request):
  if request.user.is_authenticated:
     messages.warning(request,"You are already loged in")
     return redirect('myaccount')
  elif request.method =='POST':
     email=request.POST['email']
     password=request.POST['password']
     user=auth.authenticate(email=email,password=password)
     if user is not None:
        auth.login(request,user)
        messages.success(request,"Yoy are loged in")
        return redirect('myaccount')
     else:
      messages.error(request,"Invalid credentials")
     return redirect('Login')
  return render(request,"accounts/login.html")

def logout(request):
   auth.logout(request)
   messages.info(request,"You are logged Out")
   return redirect('Login')

def dashboard(request):
   return render(request,"accounts/dashboard.html")
@login_required(login_url='Login')
 
def myaccount(request):
    user = request.user
    redirecturl = detectuser(user)

    if redirecturl:  # Ensure it's not None
        return redirect(redirecturl)
    
    return redirect('dashboard')  # Default fallback

# @login_required(login_url='Login')
# def myaccount(request):
#    user=request.user
#    redirecturl=detectuser(user)
#    return redirect(redirecturl)
 
@login_required(login_url='Login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
   return render(request,'accounts/custDashboard.html')  # Use the correct URL name
    
@login_required(login_url='Login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
   return render(request,'accounts/vendDashboard.html')
def activate(request,uidb64,token):
   try:
      uid=urlsafe_base64_decode(uidb64).decode()
      user=User._default_manager.gey(pk=uid)
   except(TypeError,ValueError,OverflowError,User.DoesNotExist):
      user=None
   if user is not None and default_token_generator.check_token(user,token):
      user.is_active=True
      user.save()
      messages.success(request,'Congrats your account is activated')
      return redirect('myaccount')
   else:
      messages.error(request,'invlaid')
      return redirect('myaccount')
   
def forgot_password(request):
   if request.method=='POST':
      email=request.POST['email']
      if User.objects.filter(email=email).exists():
         user=User.objects.get(email_exact=email)
         mail_subject='Reset Password'
         email_template='accounts/email/reser_password_email.html'
      
         send_verification_email(request,user,mail_subject,email_template)
         messages.success(request,'password link as sent ')
         return redirect('Login')
      else:
         messages.error(request,'Account does not exit')
         return redirect('forget_password')
   return  render(request,'accounts/forgot_password.html')
def reset_password_validate(request,uidb64,token):
      try:
         uid=urlsafe_base64_decode(uidb64).decode()
         user=User._default_manager.gey(pk=uid)
      except(TypeError,ValueError,OverflowError,User.DoesNotExist):
         user=None
      if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.info(request,'please reset your password')
        return redirect('reset_password')
      else:
         messages.error(request,'link as been expired')
         return redirect('myaccount')
def reset_password(request):
   if request.method=='POST':
      password=request.POST['password']
      confirm_password=request.POST['confirm_password']
      if password==confirm_password:
         pk=request.session.get('uid')
         user=User.objects.get(pk=pk)
         user.set_password(password)
         user.is_active=True
         user.save()
         messages.success(request,'Password reset successfully')
         return redirect('Login')
   return render(request,'accounts/reset_password.html')