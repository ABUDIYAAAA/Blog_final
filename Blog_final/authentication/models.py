from django.db import models
from django.contrib.auth.models import User
from blog.models import Post
from ckeditor.fields import RichTextField
from PIL import Image
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    age = models.IntegerField(default=0)
    profile_picture = models.ImageField(default="default.png", upload_to="images/profile/")
    bio = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
