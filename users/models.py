from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from dotpy.core.utils import generate_code

import logging

logger = logging.getLogger(__name__)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    email_verified = models.BooleanField(default=False)
    confirm_code = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(max_length=64, null=True, blank=True)
    
    def __unicode__(self):
        return u'%s' % self.user.username

def create_user_profile(sender, instance=None, **kwargs):
    if instance and kwargs.get('created', False):
        confirm_code = generate_code(20)
        while UserProfile.objects.filter(confirm_code=confirm_code).exists():
            logger.warning('Confirm-code exists in database: %s' % confirm_code)
            confirm_code = generate_code(20)
        profile = UserProfile(user=instance, confirm_code=confirm_code)
        profile.save()

post_save.connect(create_user_profile, sender=User)
