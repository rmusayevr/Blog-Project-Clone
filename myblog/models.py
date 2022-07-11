from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_at = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(is_approved = True)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk":self.pk})

    def __str__(self):
        return f"{self.author}'s post"

class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def approve(self):
        self.is_approved = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return f"{self.author}'s comment"
