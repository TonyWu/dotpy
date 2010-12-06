from django.http import Http404
from django.shortcuts import render_to_response
import logging as log
from dotpy.lessons.models import Lesson, Comment

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

def _check_markdown_cache(lesson):
  '''
  Check if the cache file exists for this lesson.
  If not, create one with the results of Markdown processing.
  The "cache file" means the resulting HTML content of the
  Markdown source of the lesson.
  '''
  import os
  from os import path
  base_dir = path.abspath(path.dirname(__file__))
  # first, check the cache directory
  cache_dir = path.join(base_dir, 'templates/cache/')
  if not path.exists(cache_dir):
    os.mkdir(cache_dir)
  markdown_template = '%s.html' % lesson.slug
  cache_file = path.join(cache_dir, markdown_template)
  # now check the cache file, if not exist, create it
  if not path.exists(cache_file):
    import markdown
    import codecs
    # process with Markdown
    cache_content = markdown.markdown(lesson.content)
    cache_output = codecs.open(cache_file, 'wU', 'utf-8')
    cache_output.write(cache_content)
    cache_output.close()
  # now the HTML file should exist
  # build the template file name to be included in the template
  markdown_template = 'cache/%s' % markdown_template
  return markdown_template

def show(request, lesson_slug):
  if not lesson_slug:
    # show lessons home page
    return render_to_response('home.html')

  # load lesson from database
  lesson = _load_by_slug(lesson_slug)

  # check if the cache file exists for this lesson
  markdown_template = _check_markdown_cache(lesson)
  return render_to_response('lesson.html', \
            {'lesson':lesson, \
             'comments_num': lesson.comment_set.count(), \
             'markdown_template': markdown_template
            })

def show_comments(request, lesson_slug):
  lesson = _load_by_slug(lesson_slug)
  comments = lesson.comment_set.all()
  return render_to_response('comment.html', {'lesson': lesson, 'comments': comments})
