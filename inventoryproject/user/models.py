from django.db import models
from dashboard.models import Location, User
from PIL import Image
from django.conf import settings

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE) #associating user model to django users, existing users present so has to be true , #CASCADE - deleting user will delete other stuff automatically
    location = models.ForeignKey('dashboard.Location', on_delete=models.CASCADE, null=True)  
    image = models.ImageField(upload_to='profile_image', blank = True) #upload_to = 'path for saving', blank
    #ImageField is dependent on Pillow, run 'pip install pillow' on your cmd prompt

    def __str__(self): #self is the instance
        return f'{self.user.username} Profile' #f string print