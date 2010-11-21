from django.db import models
from django.contrib.auth.models import User

class Lesson(models.Model):
  subject = models.CharField(max_length=100)
  summary = models.CharField(max_length=500)

class Article(models.Model):
  title = models.CharField(max_length=100)
  content = models.CharField(max_length=3000)
  of_lesson = models.ForeignKey(Lesson)
  of_article = models.ForeignKey('self')
 
class Comment(models.Model):
  content = models.CharField(max_length=200)
  author = models.ForeignKey(User)
  article = models.ForeignKey(Article)
