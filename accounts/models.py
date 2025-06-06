from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from django.contrib.auth.models import User
from django.db import models

from django.conf import settings
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email :
            raise ValueError('email must exit')
        if not username :
            raise ValueError('username must exit')
        user=self.model(email=self.normalize_email(email),
                        username=username,first_name=first_name,last_name=last_name,)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,first_name,last_name,username,email,password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_supperadmin=True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser):
        RESTAURANT=1
        CUSTOMER=2
        ROLE_CHOICE=((RESTAURANT,'Restaurant'),
                     (CUSTOMER,'customer'),)
        first_name=models.CharField(max_length=50)
        last_name=models.CharField(max_length=50)
        username=models.CharField(max_length=50 ,unique=True)
        email=models.EmailField(max_length=100 ,unique=True)
        phone_number=models.CharField(max_length=10,blank=True)
        role=models.PositiveSmallIntegerField(choices=ROLE_CHOICE,blank=True ,null=True)
        date_joinied=models.DateTimeField(auto_now_add=True)
        lost_login=models.DateTimeField(auto_now=True)
        created_date=models.DateTimeField(auto_now=True)
        modified_date=models.DateTimeField(auto_now=True)
        is_admin=models.BooleanField(default=False)
        is_staff=models.BooleanField(default=False)
        is_active=models.BooleanField(default=False)
        is_superadmin=models.BooleanField(default=False)
        USERNAME_FIELD='email'
        REQUIRED_FIELDS=['username','first_name','last_name']
        objects=UserManager()
        def __str__(self):
            return self.email
        def has_perm(self,perm,obj=None):
            return self.is_admin
        def has_module_perms(self,app_label):
            return True
        def get_role(self):
             if self.role == 1:
                 user_role='vendor'
             elif self.role == 2: 
                 user_role= 'customer'
             return user_role
 

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Corrected reference
    #profile_picture = models.ImageField(upload_to='user/profile_pictures', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='media/user/profile_pictures/')
    cover_photo = models.ImageField(upload_to='media/user/cover_photo', blank=True, null=True)
    address_line_1 = models.CharField(max_length=100, blank=True, null=True)
    address_line_2 = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    pin_code = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username  # Display username properly
     
 
#post_save.connect(post_save_create_profile_reciever,sender=User)


     











                        