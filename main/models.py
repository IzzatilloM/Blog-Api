from django.db import models
from django.contrib.auth.models import User

class PublishedManager(models.Manager):
    def get_queryset(self):
        super().get_queryset().filter(published=True)

class Article(models.Model):
    title = models.CharField(max_length=255)
    cover = models.ImageField(upload_to='articles/', blank=True, null=True)
    context = models.TextField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    objects = models.Manager()
    published_data = PublishedManager()

    def __str__(self):
        return f"{self.user.username} | {self.title}"