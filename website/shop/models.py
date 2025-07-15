from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True, verbose_name='Название')
    slug = models.SlugField(verbose_name='Слаг', 
        help_text='Данное поле заполняется автоматически'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(verbose_name='Слаг', null=True, blank=True) 
    preview = models.ImageField(upload_to='products/previews/', null=True, blank=True, verbose_name='Превью')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.author} - {self.product}'
        
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзовы'
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    photo = models.ImageField(upload_to='products/gallery/', verbose_name='Фото')
    
    class Meta:
        verbose_name = 'Галлерея товара'
        verbose_name_plural = 'Галлерея товаров'   
    

class InstagramImage(models.Model):
    image = models.ImageField(upload_to='instagram/')
    username = models.CharField(max_length=100, default='ashion_shop')

    def __str__(self):
        return f"Instagram Image {self.id}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} ❤ {self.product.title}"

