from django.db import models

# Create your models here.
class Room(models.Model):
    name=models.CharField(max_length=225)
    slug=models.SlugField(unique=True) # A slug is a short, human-readable, and unique identifier for a web page or resource. It's typically used in the URL of a web page to make it more user-friendly and SEO-friendly. For example, in a blog post URL like "https://example.com/blog/my-awesome-post/", the slug would be "my-awesome-post"