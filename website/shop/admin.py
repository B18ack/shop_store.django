from django.contrib import admin
from . import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'slug', 'created_at']  
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ['pk', 'name']  
    list_filter = ['created_at']
    search_fields = ['name']

class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 1

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline]

admin.site.register(models.InstagramImage)
