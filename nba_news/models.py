from django.db import models

# Create your models here.
class NBANews(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class NBANewsDetail(models.Model):
    nba_news = models.ForeignKey(NBANews, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)