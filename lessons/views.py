from django.http import Http404
from django.shortcuts import render_to_response, redirect
import logging as log
from dotpy.lessons.models import Lesson, Comment, LessonForm
from django.template.context import RequestContext
from dotpy.lessons.util import _check_markdown_cache

def home(request):
  lessons = Lesson.objects.all()
  return render_to_response('home.html', {'lessons': lessons})

def _load_by_slug(slug):
  """
  Load an object (type of Lesson) from the database,
  whose slug equals the given one.
  Note: Http404 exception will be raised if such object
  can not be found or multiple objects found.

  # Create some lessons
  >>> a = Lesson.objects.create(subject='Subject A', slug='a',
  ...     summary='Summary A', content='Content A')
  >>> b = Lesson.objects.create(subject='Subject B', slug='b',
  ...     summary='Summary B', content='Content B')
  >>> b2 = Lesson.objects.create(subject='Subject B', slug='b',
  ...     summary='Summary B', content='Content B')

  # Load by slug
  # OK
  >>> _a = _load_by_slug('a')
  >>> _a.subject
  u'Subject A'
  >>> _a.slug
  u'a'
  >>> _a.summary
  u'Summary A'
  >>> _a.content
  u'Content A'

  # Not found
  >>> tmp = _load_by_slug('not-found')
  Traceback (most recent call last):
    ...
  Http404

  # Duplicate lessons foud with the given slug
  >>> _b = _load_by_slug('b')
  Traceback (most recent call last):
  Http404
  """
  try:
    obj = Lesson.objects.get(slug=slug)
  except Lesson.DoesNotExist:
    raise Http404()
  except Lesson.MultipleObjectsReturned:
    log.error('Duplicate slug for lesson found: %s' % slug)
    raise Http404()
  return obj

def show(request, slug):
  if not slug:
    # show lessons home page
    return render_to_response('home.html')

  # load lesson from database
  lesson = _load_by_slug(slug)

  # check if the cache file exists for this lesson
  markdown_template = _check_markdown_cache(lesson)
  return render_to_response('lesson.html', \
            {'lesson':lesson, \
             'comments_num': lesson.comment_set.count(), \
             'markdown_template': markdown_template
            })

def show_comments(request, slug):
  lesson = _load_by_slug(slug)
  comments = lesson.comment_set.all()
  return render_to_response('comment.html', {'lesson': lesson, 'comments': comments})

def edit(request, slug):
  # TODO admin required
  if request.method == 'POST':
    lesson = _load_by_slug(slug)
    form = LessonForm(request.POST, instance=lesson)
    if form.is_valid():
      form.save()
      return redirect('/learn/%s' % slug)
  else:
    if slug:
      lesson = _load_by_slug(slug)
      form = LessonForm(instance=lesson)
    else:
      form = LessonForm()
    return render_to_response('lesson_form.html', {'form': form}, RequestContext(request))