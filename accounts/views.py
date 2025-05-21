from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from accounts.forms import UserForm
from accounts.models import User, UserProfile
from vendor.forms import VendorForm
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