from django.contrib import admin
from .models import Post, Image

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1  # Количество пустых полей для добавления изображений

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_posted']
    search_fields = ['title', 'content']
    list_filter = ['date_posted', 'author']
    inlines = [ImageInline]

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'image']