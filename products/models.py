from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    category_name = models.CharField(max_length=150)
    category_image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    category_slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)

    @staticmethod
    def generate_slug(model, name):
        base_slug = slugify(name)
        slug = base_slug
        counter = 1

        while model.objects.filter(category_slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.category_slug:
            self.category_slug = self.generate_slug(Category, self.category_name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name

class Brand(models.Model):
    brand_name = models.CharField(max_length=255)
    brand_image = models.ImageField(upload_to='brand_images/', blank=True, null=True)
    brand_slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    @staticmethod
    def generate_slug(model, name):
        base_slug = slugify(name)
        slug = base_slug
        counter = 1

        while model.objects.filter(brand_slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.brand_slug:
            self.brand_slug = self.generate_slug(Brand, self.brand_name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.brand_slug
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete = models.CASCADE, related_name='brand')
    product_name = models.CharField(max_length=200)
    product_slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    product_image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    product_description = models.TextField()
    product_price = models.PositiveIntegerField(default=0)
    product_inventory = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    original_price = models.PositiveIntegerField(null=True, blank=True)
    discounted_price = models.PositiveIntegerField(null=True, blank=True)
    has_discounted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    @staticmethod
    def generate_slug(model, name):
        base_slug = slugify(name)
        slug = base_slug
        counter = 1

        while model.objects.filter(product_slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug
    

    def save(self, *args, **kwargs):
        if not self.product_slug:
            self.product_slug = self.generate_slug(Product, self.product_name)
        if self.has_discounted:
            if not self.original_price or not self.product_price:
                raise ValueError("Discounted Products must have prices")
            elif self.discounted_price >= self.original_price:
                raise ValueError("Discounted prices should be less")
        else:
            self.original_price = None
            self.discounted_price = None
                
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.category_name} - {self.product_name}"
