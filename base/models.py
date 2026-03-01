from django.db import models
from ckeditor.fields import RichTextField 
# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.name.startswith('#'):
            self.name = '#' + self.name.lower()
        super().save(*args, **kwargs)

class News(models.Model):
    title = models.CharField(max_length=255)
    tags =models.ManyToManyField(Tag, related_name='news', blank=True)
    images = models.ImageField(upload_to='news_images/')
    slug = models.SlugField(max_length=255, unique=True)
    content = RichTextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

