from django.shortcuts import render_to_response

def home(request):
  return render_to_response('lessons_home.htm')

def learn_python(request, title_slug):
  if not title_slug:
    return render_to_response('python/home.htm')
  else # TODO show an article
    return render_to_response('python/home.htm')

def learn_django(request, title_slug):
  if not title_slug:
    return render_to_response('django/home.htm')
  else # TODO show an article
    return render_to_response('django/home.htm')
