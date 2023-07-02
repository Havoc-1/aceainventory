from django.db import models
from django.contrib.auth.models import User
from dashboard.models import Location
from PIL import Image

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE) #associating user model to django auth, existing users present so has to be true , #CASCADE - deleting user will delete other stuff automatically
    location = models.ForeignKey('dashboard.Location', on_delete=models.CASCADE, null=True, blank = True) 
    image = models.ImageField(upload_to='profile_image', blank = True) #upload_to = 'path for saving', blank
    #ImageField is dependent on Pillow, run 'pip install pillow' on your cmd prompt

    def __str__(self): #self is the instance
        return f'{self.user.username} Profile' #f string print