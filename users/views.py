# encoding=utf8

import logging

from django.http import Http404
from django.template.context import RequestContext
from django.shortcuts import render_to_response, redirect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from dotpy.users.models import UserProfile
from dotpy.core.utils import render_to_json, render_to_json_err, check_post_json, is_valid_email, get_or_none, send_email

logger = logging.getLogger(__name__)

def signin(request):
    '''
    User signin.
    
    *POST Parameters*
    
      ``username`` - The username or email address.

      ``password`` - The password.

      ``code`` - CAPTCHA code, TODO
    
    *URL Name* - ``signin``.
    
    *Template Name* - ``signin.html``.
    '''
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if not (username and password):
            messages.error(request, u'登录信息不完整！')
        else:
            if is_valid_email(username):
                found = get_or_none(User, email=username)
                if found:
                    username = found.username
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(request.POST.get('next', '/'))
                else:
                    messages.error(request, u'账号被锁定，无法登录！')
            else:
                messages.error(request, u'登录信息不正确！')
    else: # request.method is "GET"
        if request.user.is_authenticated():
            return redirect(request.POST.get('next', '/'))

    return render_to_response('users/signin.html', context_instance=RequestContext(request))

def forgot_password(request):
    '''
    Show a form to the user for him to input the username/email.
    If the username/email is found in the databse, send an email to the user's email address including the link for resetting his/her password.

    *POST Parameters*

      ``username`` - The username or email address.

    *URL Name* - ``forgot-password``.

    *Template Name* - ``forgot_password.html``.
    '''
    # TODO
    # Note: inactive user can NOT trigger forgot-password.
    return render_to_response('users/forgot_password.html')

def signout(request):
    '''
    Sign out a user.
    
    ``URL Name`` - "signout"
    '''
    logger.info('Signout user... %s', request.user)
    logout(request)
    return redirect('/')

def _generate_username():
    num = 1000
    print 'num: %d' % num
    while get_or_none(User, username=str(num)):
        num = num + 1
        print 'num: %d' % num
    return str(num)

def signup(request):
    '''
    User signup.
    
    *URL Name* - ``signup``.
    
    *POST Parameters*
    
      ``email`` - The user's email address.
    
    *URL Name* - ``user-signup``.

    *Template Name* - ``signup.html``.
    '''
    if request.method == 'POST':
        email = request.POST.get('email', None)
        if not email:
            messages.error(request, u'请输入电子邮箱！')
        elif not is_valid_email(email):
            messages.error(request, u'电子邮箱格式不正确！')
        else:
            user = get_or_none(User, email=email)
            if user:
                messages.error(request, u'账号已存在，请登录或使用另一个电子邮箱')
            else:
                username = _generate_username()
                user = User(email=email, username=username)
                user.save()
                confirm_code = user.get_profile().confirm_code
                confirm_link = reverse('user-confirm-signup', args=[confirm_code])
                send_email(email, 'signup', context=dict(confirm_link=confirm_link))
                messages.success(request, _('Registratoin submitted! Check your email to for further instructions.'))
    else: # request.method is "GET"
        if request.user.is_authenticated():
            return redirect(request.POST.get('next', '/'))
    
    return render_to_response('users/signup.html', context_instance=RequestContext(request))

def confirm_signup(request, code):
    '''
    Confirm a signup. Typically by clicking the link in the email received after signing up.

    *Context Variables*

      ``code`` - The confirmation code.

    *URL Name* - ``user-confirm-signup``.

    *Template Name*

      ``core/broken_link.html``, if the code is not valid.

      ``users/reset_password.html``, if the code is valid, and a form will be shown for the user to set his password.
    '''
    if not code:
        raise Http404
    
    user_profile = get_or_none(UserProfile, confirm_code=code)
    if not user_profile:
        return render_to_response('core/broken_link.html')
    else:
        if user_profile.email_verified: # Already confirmed before
            user_profile.confirm_code = None
            user_profile.save()
            next_url = request.REQUEST.get('next', None)
            if not next_url:
                next_url = reverse('user-account')
            return redirect(next_url)
        else:
            user_profile.email_verified = True
            user_profile.save()
            # Redirect the user to the reset-password page so that he can set his password.
            return redirect('user-reset-password', code=code)

def reset_password(request, code):
    '''
    Update user's password if the confirmation code is valid.

    *Context Variables*

      ``code`` - The confirmation code.

    *POST Variables*

      ``code`` - The confirmation code (should be the same with the code of the URL parameters).

      ``email`` - The email of the user.

      ``password1`` - The new password.

      ``password2`` - The password to be confirmed.

    *Template Name* 

      ``core/broken_link.html`` - if the confirmation code is invalid or the user is inactive (locked).
    
      ``reset_password.html`` - if the HTTP method is "GET". Available context: ``user_profile``.

      Redirected to "next URL" or "my account" page if the HTTP method is "POST".

    '''
    if not code:
        raise Http404

    user_profile = get_or_none(UserProfile, confirm_code=code)
    # If the confirmation code is incorrect, or the user is locked, do not allow resetting password.
    if not (user_profile and user_profile.user.is_active):
        return render_to_response('core/broken_link.html')

    if request.method == 'POST':
        confirm_code = request.POST.get('code', None)
        email = request.POST.get('email', None)
        password1 = request.POST.get('password1', None)
        password2 = request.POST.get('password2', None)

        if not confirm_code or confirm_code != user_profile.confirm_code or email != user_profile.user.email:
            return render_to_response('core/broken_link.html')
        
        if not password1 or not password2 or password1 != password2:
            messages.error(request, _('Make sure the passwords are entered and match each other.'))
        else:
            password_len = len(password1)
            if password_len < 3 or password_len > 30:
                messages.error(request, _('The length of password should be between 3 and 30.'))
            else:
                user = user_profile.user
                user.set_password(password1)
                user.save()
                user_profile.confirm_code = None
                user_profile.save()
                # Log the user in
                user = authenticate(username=user.username, password=password1)
                login(request, user)
                next_url = request.POST.get('next', None)
                if not next_url:
                    next_url = reverse('user-account')
                return redirect(next_url)

    return render_to_response('users/reset_password.html', {'user_profile': user_profile}, context_instance=RequestContext(request))

@login_required
def my_account(request):
    # TODO
    logger.warning('----- Accessing my_account.')
    return redirect('/learn/')

