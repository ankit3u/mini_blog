from django.contrib import admin
from .models import Blog, Post

# Register your models here.
@admin.register(Post)

class PostModelAdmin(admin.ModelAdmin):
    list_display=['id','title','desc']

    
admin.site.register(Blog)