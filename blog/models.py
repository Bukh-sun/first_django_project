from django.conf import settings
from django.db import models
from django.db.models import F
from django.urls import reverse
from django.utils import timezone

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published_date__isnull=False)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    published_date = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    views_count = models.PositiveIntegerField(default=0)
    # tags = models.ManyToManyField('Tag', blank=True, related_name='posts')

    objects = models.Manager()
    published = PublishedManager()

    def increment_views(self):
        Post.published.filter(pk=self.pk).update(views_count=F('views_count') + 1)
        self.refresh_from_db()

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.author} commented on {self.post}'


