from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=200)
    parent = models.ForeignKey(
        "self", blank=True, null=True,
        related_name="child", on_delete=models.CASCADE
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.parent} --> {self.title}" if self.parent else self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    image = models.ImageField(upload_to="media/", blank=True, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_image")

    def __str__(self):
        return self.product.title

