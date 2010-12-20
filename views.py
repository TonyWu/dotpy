from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
import logging as log
from dotpy.util import User, SessionKey
from dotpy import settings

def notify(request):
  return render_to_response('_index.htm')

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
def rpx(request, token):
  import urllib
  import urllib2
  import json

  api_params = {
    'token': token,
    'apiKey': 'bfd67c0c106bec8ad859890ff16e31e609fd3aa3',
    'format': 'json',
  }

  # make the api call
  http_response = urllib2.urlopen('https://rpxnow.com/api/v2/auth_info',
                                  urllib.urlencode(api_params))

  # read the json response
  auth_info_json = http_response.read()

  # Step 3) process the json response
  auth_info = json.loads(auth_info_json)

  # Step 4) use the response to sign the user in
  if auth_info['stat'] == 'ok':
    profile = auth_info['profile']
  
    # 'identifier' will always be in the payload
    # this is the unique idenfifier that you use to sign the user
    # in to your site
    identifier = profile['identifier']
  
    # these fields MAY be in the profile, but are not guaranteed. it
    # depends on the provider and their implementation.
    name = profile.get('displayName')
    email = profile.get('email')
    profile_pic_url = profile.get('photo')

    # actually sign the user in.  this implementation depends highly on your
    # platform, and is up to you.
    sign_in_user(request, identifier, name, email, profile_pic_url)
  else:
    log.error('OpoenID RPX failed: ' + auth_info['err']['msg'])
    
  return redirect('/')
