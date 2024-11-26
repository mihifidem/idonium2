from django.contrib.auth.models import User
from django.db import models

STATUS = ((0, "Draft"), (1, "Publish"))

class CategoryPost (models.Model):
    nameCategoryPost = models.CharField(max_length=100)
    def __str__(self):
        return self.nameCategoryPost


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    likes = models.IntegerField(null=True, blank=True,default=0)
    category_post = models.ForeignKey(CategoryPost, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)  # Nuevo campo de imagen

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField(null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("post_detail", kwargs={"slug": str(self.slug)})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return "Comment {} by {}".format(self.body, self.name)
