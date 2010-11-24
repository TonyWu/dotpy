from django.db import models
from django.contrib.auth.models import User

class Lesson(models.Model):
	subject = models.CharField(max_length=100)
	summary = models.CharField(max_length=500)

	def __unicode__(self):
		return self.subject;

class Article(models.Model):
	title = models.CharField(max_length=100)
	content = models.CharField(max_length=3000)
	of_lesson = models.ForeignKey(Lesson)
	of_article = models.ForeignKey('self', blank=True, null=True)

	def __unicode__(self):
		return self.title;

class Comment(models.Model):
	content = models.CharField(max_length=200)
	author = models.ForeignKey(User)
	article = models.ForeignKey(Article)

	def __unicode__(self):
		return self.author.getFullName();
