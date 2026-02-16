from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    views_count = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class CalculationLog(models.Model):
    calculator_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


class Lead(models.Model):
    email = models.EmailField(unique=True)
    source = models.CharField(max_length=100, default='newsletter')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        self.email