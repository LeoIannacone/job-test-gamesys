from __future__ import unicode_literals

from django.db import models


class Webhooks(models.Model):
    status = models.TextField(default='')
    data = models.TextField()
