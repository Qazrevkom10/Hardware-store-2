from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    poster = models.ImageField(upload_to="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})


class Electronica(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products")
    price = models.PositiveIntegerField()
    description = models.TextField()
    count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('single_electronica', kwargs={"cat_slug": self.category.slug, "slug": self.slug})


ELECTRONICA_MADE_IN = (
    ("USA", "USA"),
    ("Germany", "Germany"),
    ("China", "China"),
    ("Japan", "Japan"),
)


class Order(models.Model):
    product = models.ForeignKey(Electronica, on_delete=models.SET_NULL, null=True, blank=True)
    costumer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveSmallIntegerField(default=1)
    made_in = models.CharField(max_length=50, choices=ELECTRONICA_MADE_IN, null=True, blank=True)
    isSelling = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pk
