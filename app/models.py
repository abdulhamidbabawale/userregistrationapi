from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    user_id= models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=24, blank=True,null=True)
    profile_pic = CloudinaryField('image' ,folder='user_management_api_profile-pic' )
    address = models.CharField(max_length= 255, blank=True ,null=True)
    city = models.CharField(max_length= 255, blank=True)
    state = models.CharField(max_length= 255, blank=True)
    Country = models.CharField(max_length= 255, blank=True)



