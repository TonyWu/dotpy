from django.http import Http404
from django.shortcuts import render_to_response
import logging as log
from dotpy.lessons.models import Lesson, Article

def home(request):
  return render_to_response('home.htm')

def _load_with_slug(model, slug):
  '''
  Load an object (type of model) from the database,
  whose slug equals the given one.
  Note: Http404 exception will be raised if such object
  can not be found or multiple objects found.
  '''
  try:
    obj = model.objects.get(slug=slug)
  except model.DoesNotExist:
    raise Http404()
  except model.MultipleObjectsReturned:
    log.error('Duplicate slug for %s: %s' % (model, slug))
    raise Http404()
  return obj

def show(request, lesson_slug, article_slug):
  if not lesson_slug:
    # show lessons home page
    return render_to_response('home.htm')

  # load lesson from database
  lesson = _load_with_slug(Lesson, lesson_slug)

  if not article_slug:
    # show lesson summary and table of contents
    return render_to_response('lesson.htm', {'lesson':lesson})

  # load article from database
  article = _load_with_slug(Article, article_slug)
  return render_to_response('article.htm')

def learn_django(request, title_slug):
  if not title_slug:
    return render_to_response('django/home.htm')
  else: # TODO show an article
    return render_to_response('django/home.htm')
