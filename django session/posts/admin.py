from django.contrib import admin
from .models import Post, Comment

# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment
    
class PostInline(admin.ModelAdmin):
    inlines = {
        CommentInline,
    }
    
admin.site.register([Post, Comment])