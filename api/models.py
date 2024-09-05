from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    text = models.CharField(max_length=1500, blank=True)
    created_at = models.DateTimeField(null=True)
    is_new_post = models.BooleanField(default=False)
    col = models.IntegerField(default=1)

    def __str__(self):
        return self.text

class Comment(models.Model):
    text = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.text

class Image(models.Model):
    file = models.ImageField(upload_to="post-images", max_length=255)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')

    def save(self, *args, **kwargs):
        super().save()

class Attachment(models.Model):
    MUSIC = 'music'
    MOVIE = 'movie'
    BOOK = 'book'
    GAME = 'game'
    LINK = 'link'
    TYPES_CHOICES = [
        (MUSIC, 'music'),
        (MOVIE, 'movie'),
        (BOOK, 'book'),
        (GAME, 'game'),
        (LINK, 'link'),
    ]
    type = models.CharField(
        max_length=6,
        choices=TYPES_CHOICES,
        default=MUSIC
    )
    text = models.CharField(max_length=90)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='attachments')

    def __str__(self):
        return self.text

class Customization(models.Model):
    type = models.CharField(max_length=28)
    content = models.CharField(max_length=250, blank=True)
    file = models.ImageField(upload_to="site-illustrations", blank=True)

    def __str__(self):
        return self.type

    def save(self, *args, **kwargs):
        super().save()

class Tag(models.Model):
    name = models.CharField(max_length=90)

    def __str__(self):
        return self.name
        
class Subscribe(models.Model):
    url = models.CharField(max_length=120)
    last_post_id = models.IntegerField(blank=True)
    last_article_id = models.IntegerField(blank=True)

    def __str__(self):
        return self.url

class Article(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=300, blank=True)
    text = models.CharField(max_length=15000)
    created_at = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(upload_to="article-images", blank=True)
    tags = models.ManyToManyField(Tag, blank='True')

    def save(self, *args, **kwargs):
        super().save()
    
    def __str__(self):
        return self.title

class ArticleComment(models.Model):
    text = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_comments')

    def __str__(self):
        return self.text
       
class Smile(models.Model):
    file = models.ImageField(upload_to='smiles/')

