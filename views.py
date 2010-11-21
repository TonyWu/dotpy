from django.shortcuts import render_to_response

def notify(request):
    return render_to_response('_index.htm')

def index(request):
    return render_to_response('root/index.htm')

def article(request):
    return render_to_response('root/article.htm')
