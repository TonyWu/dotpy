from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea
from dotpy.lessons.util import check_lesson_markdown_cache

class Lesson(models.Model):
	subject = models.CharField(max_length=100)
	slug = models.CharField(max_length=30, unique=True)
	summary = models.CharField(max_length=500)
	content = models.TextField(max_length=99999)

	def __unicode__(self):
		return self.subject
	
	def save(self, *args, **kwargs):
		super(Lesson, self).save(*args, **kwargs)
		check_lesson_markdown_cache(self, True)

class Comment(models.Model):
	content = models.CharField(max_length=200)
	created_on = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(User)
	lesson = models.ForeignKey(Lesson)

	def __unicode__(self):
		return self.author.get_full_name();

class LessonForm(ModelForm):
  class Meta:
  	model = Lesson
  	widgets = {
				'summary': Textarea({'cols': 100, 'rows': 5}),
				'content': Textarea({'cols': 100, 'rows': 30}),
		}
