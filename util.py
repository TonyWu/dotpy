# encoding=utf8

class User:
  """
  Represents dotPy users.
  """
  
  def __init__(self, identifier, name, email, profile_pic_url):
    self.identifier = identifier
    self.name = name
    self.email = email
    self.profile_pic_url = profile_pic_url
    
  def __str__(self):
    return '%s - %s' % (self.identifier, self.name)


class SessionKey:
  """
  Keys for data stored in the HTTP session.
  """
  USER = 'dotpy_user'
  

from django.template.context import RequestContext

def user_context(request):
  return RequestContext(request, {'dotpy_user': request.session.get(SessionKey.USER, None)})
