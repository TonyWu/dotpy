from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from dotpy.lessons.models import Lesson, Comment, LessonForm
from dotpy.lessons.utils import check_lesson_markdown_cache

def home(request):
  lessons = Lesson.objects.all()
  return render_to_response('lessons/home.html', {'lessons': lessons}, RequestContext(request))

def show(request, slug):
  if not slug:
    # show lessons home page
    return render_to_response('lessons/home.html')
  
  # load lesson from database
  lesson = get_object_or_404(Lesson, slug=slug)
  
  # check if the cache file exists for this lesson
  markdown_template = check_lesson_markdown_cache(lesson)
  return render_to_response('lessons/lesson.html', \
            {'lesson':lesson, \
             'comments_num': lesson.comment_set.count(), \
             'markdown_template': markdown_template \
            }, RequestContext(request)(request))

def show_comments(request, slug):
  lesson = get_object_or_404(Lesson, slug=slug)
  comments = lesson.comment_set.all()
  return render_to_response('lessons/comment.html',
            {'lesson': lesson, 'comments': comments},
            RequestContext(request)(request))

@login_required
def edit(request, slug):
  # TODO admin required
  if request.method == 'POST':
    if slug:
      lesson = get_object_or_404(Lesson, slug=slug)
      form = LessonForm(request.POST, instance=lesson)
    else:
      form = LessonForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('/learn/%s' % form.instance.slug)
  else:
    if slug:
      lesson = get_object_or_404(Lesson, slug=slug)
      form = LessonForm(instance=lesson)
    else:
      form = LessonForm()
  return render_to_response('lessons/lesson_form.html', {'form': form}, RequestContext(request)(request))
