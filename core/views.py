# encoding=utf8

from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from dotpy.core.utils import render_to_json, render_to_json_err, check_post_json, is_valid_email, get_or_none, send_email

def notify(request):
  return render_to_response('core/index.html')

def signin(request):
    '''
    Try to sign in a user.
    POST only.
    
    ``URL Name`` - "signin"
    
    ``POST Parameters``
    
      ``username``
      ``password``
      ``code`` - CAPTCHA code, TODO
    
    ``Returns`` - JSON dict: error message in r['err'] when failed, otherwise empty.
    '''
    result = check_post_json(request)
    if result:
        return result
    
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    if not (username and password):
        return render_to_json_err(u'登录信息不完整！')
    
    if is_valid_email(username):
        found = get_or_none(User, email=username)
        if found:
            username = found.username
        else:
            return render_to_json_err(u'登录信息不正确！')
    
    user = authenticate(username=username, password=password)
    if user:
        if user.is_active:
            login(request, user)
            return render_to_json()
        else:
            return render_to_json_err(u'账号被锁定，无法登录！')
    else:
        return render_to_json_err(u'登录信息不正确！')

def signout(request):
    '''
    Sign out a user.
    
    ``URL Name`` - "signout"
    '''
    logout(request)
    return render_to_json()

def _generate_username():
    num = 1000
    print 'num: %d' % num
    while get_or_none(User, username=str(num)):
        num = num + 1
        print 'num: %d' % num
    return str(num)

def signup(request):
    '''
    Try to sign up a user.
    POST only.
    
    ``URL Name`` - "signup"
    
    ``POST Parameters``
    
      ``email`` - The user's email address.
    
    ``Returns`` - JSON dict: error message in r['err'] when failed, otherwise empty.
    '''
    result = check_post_json(request)
    if result:
        return result
    
    email = request.POST.get('email', None)
    if not email:
        return render_to_json_err(u'请输入电子邮箱！')
    
    if not is_valid_email(email):
        return render_to_json_err(u'电子邮箱格式不正确！')
    
    user = get_or_none(User, email=email)
    if user:
        return render_to_json_err(u'账号已存在，请登录或使用另一个电子邮箱')
    
    username = _generate_username()
    user = User(email=email, username=username)
    user.save()
    confirm_code = user.get_profile().confirm_code
    confirm_link = reverse('confirm-signup', args=[confirm_code])
    send_email(email, 'signup', context=dict(confirm_link=confirm_link))
    
    return render_to_json(dict(info=u'请查收邮件。'))

def confirm(request):
    # TODO
    return render_to_json()

