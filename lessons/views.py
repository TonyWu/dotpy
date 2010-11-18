from django.shortcuts import render_to_response

def home(request):
    return render_to_response('lessons_home.htm')

def learn_python(request):
    return render_to_response('python/home.htm')

def learn_django(request):
    return render_to_response('django/home.htm')
