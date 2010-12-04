from django.shortcuts import render_to_response

def notify(request):
    return render_to_response('_index.htm')
