from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=150)
    desc=models.TextField()


class Blog(models.Model):
    title = models.CharField(max_length=200)
    image = CloudinaryField('image')
    desc=models.TextField()
    time = models.DateTimeField(auto_now_add = True)

