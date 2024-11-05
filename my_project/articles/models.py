from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', default=None)
    email = models.TextField(blank=True, null=True)
    saved_articles = models.ManyToManyField('Article', blank=True)

    def __str__(self):
        return self.user.username
    

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='articles')
    date_published = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=200)
    restricted = models.BooleanField(default=False)
    image = models.ImageField(upload_to='articles/images/', null=True, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article_id = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    author_id = models.ForeignKey(Profile, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0) 
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return f'Comment by {self.author} on {self.article}'

class SavedArticle(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date_saved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} saved {self.article.title}'