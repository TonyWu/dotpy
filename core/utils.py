# encoding=utf8

from django.utils import simplejson
from django.http import HttpResponse
from django.core.validators import email_re
from django.core.mail import send_mail
from django.template.loader import render_to_string

def render_to_json(data=None):
    if data is None:
        json = '{}'
    else:
        json = simplejson.dumps(data)
    return HttpResponse(json, mimetype='application/json')

def render_to_json_err(err_msg):
    return render_to_json(dict(err=err_msg))

def check_post_json(request):
    if request.method != 'POST':
        return render_to_json(dict(err='Not Supported.'))
    return None

def is_valid_email(email):
    return bool(email_re.match(email))

def get_or_none(model, **kwargs):
    obj = None
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        pass
    return obj

def send_email(to, kind, **kwargs):
    site = Site.objects.get_current()
    ctx = {
        'site': site,
    }
    ctx.update(kwargs.get('context', {}))
    
    subject = render_to_string("mail/%s/subject.txt" % kind, ctx)
    message = render_to_string("mail/%s/message.txt" % kind, ctx)
    
    send_mail(subject, message, settings.EMAIL_FROM, [to])

def generate_code(size):
    if size <= 0:
        return ''
    
    return 'TODO' # TODO
