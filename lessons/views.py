from django.http import Http404
from django.shortcuts import render_to_response
import logging as log
from dotpy.lessons.models import Lesson, Comment

def home(request):
  lessons = Lesson.objects.all()
  return render_to_response('home.htm', {'lessons': lessons})

def _load_with_slug(slug):
  '''
  Load an object (type of Lesson) from the database,
  whose slug equals the given one.
  Note: Http404 exception will be raised if such object
  can not be found or multiple objects found.
  '''
  try:
    obj = Lesson.objects.get(slug=slug)
  except Lesson.DoesNotExist:
    raise Http404()
  except Lesson.MultipleObjectsReturned:
    log.error('Duplicate slug for %s: %s' % (model, slug))
    raise Http404()
  return obj

def show(request, lesson_slug):
  if not lesson_slug:
    # show lessons home page
    return render_to_response('home.htm')

  # load lesson from database
  lesson = _load_with_slug(lesson_slug)

  return render_to_response('lesson.htm', \
            {'lesson':lesson, 'comments_num': lesson.comment_set.count()})

def show_comments(request, lesson_slug):
  lesson = _load_with_slug(lesson_slug)
  comments = lesson.comment_set.all()
  return render_to_response('comment.htm', {'lesson': lesson, 'comments': comments})
