from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
import logging as log
from dotpy.util import User, SessionKey
from dotpy import settings

def notify(request):
  return render_to_response('index.html')

def sign_in_user(request, identifier, name, email, profile_pic_url):
  """
  Create a new user with the given data
  and store into HTTP session.
  """
  user = User(identifier, name, email, profile_pic_url)
  request.session[SessionKey.USER] = user

def si(request):
  """
  --- TODO: This is testing only! Remove in production! ---
  Sign in as a test user if DEBUG is enabled.
  """
  if settings.DEBUG:
    sign_in_user(request, 'testing', 'Demo User', 'xhh@dotpy.org', None)
  return redirect('/')

def logout(request):
  """
  Remove the user from HTTP session.
  """
  try:
    del request.session[SessionKey.USER]
  except KeyError:
    pass
  return redirect('/')

@csrf_exempt
def rpx(request):
  import urllib
  import urllib2
  import json

  token = request.POST.get('token')
  if not token:
    return redirect('/')
  
  api_params = {
    'token': token,
    'apiKey': settings.DOTPY_RPX_APIKEY,
    'format': 'json',
  }

  http_response = urllib2.urlopen('https://rpxnow.com/api/v2/auth_info',
                                  urllib.urlencode(api_params))

  auth_info_json = http_response.read()
  auth_info = json.loads(auth_info_json)
  if auth_info['stat'] == 'ok':
    profile = auth_info['profile']
    identifier = profile['identifier']
    name = profile.get('displayName')
    email = profile.get('email')
    profile_pic_url = profile.get('photo')
    sign_in_user(request, identifier, name, email, profile_pic_url)
  else:
    log.error('OpoenID RPX failed: ' + auth_info['err']['msg'])
    
  return redirect('/')
