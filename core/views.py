# encoding=utf8

from django.shortcuts import render_to_response

def notify(request):
    '''
    Display a "Site under construction" notification.
    '''
    return render_to_response('core/index.html')

