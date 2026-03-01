from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=255)
    images = models.ImageField(upload_to='news_images/')
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

