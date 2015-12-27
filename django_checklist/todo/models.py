# Django
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

# Local
from django_checklist.common.models import Tag

class Checklist(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=30)
    tags = models.ManyToManyField(Tag, related_name='%(class)s')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0} - {1}'.format(self.title, self.created_at)

class Item(models.Model):
    checklist = models.ForeignKey(Checklist)
    description = models.CharField(max_length=100)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.description, self.is_complete, 
            self.created_at)
