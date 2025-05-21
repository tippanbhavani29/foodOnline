


from django.urls import path

from accounts import views


urlpatterns=[
    path("registerUser/",views.register_user,name='registerUser'),
    path("reigsterVendor/",views.register_ven,name='registerVendor'),
    path('login/',views.login,name='Login'),
    path('logout/',views.logout,name='Logout'),
    # path('dashbord/',views.dashboard,name='dashboard'),
    path('myaccount/',views.myaccount,name='myaccount'),
    

    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),
    path('customerDashboard/', views.customerDashboard, name='customerDashboard'),
   # path('adminDashboard/', views.adminDashboard, name='adminDashboard'),
]