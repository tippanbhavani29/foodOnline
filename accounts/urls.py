


from django.urls import path

from accounts import views


urlpatterns=[
    path("registerUser/",views.register_user,name='registerUser'),
    path("reigsterVendor",views.register_ven,name='registerVendor'),
]