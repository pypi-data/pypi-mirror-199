from django.db import models
from django.contrib.auth.models import User

class Log(models.Model):
    username = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.CharField(max_length=255)
    is_private = models.BooleanField(default=False, null=True, blank=True)
    priv_address = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    action = models.CharField(max_length=255, blank=True, null=True)
    device = models.CharField(max_length=255, blank=True, null=True)
    field_id = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    isp = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    hashed = models.CharField(max_length=32, null=True)

    def __str__(self):
        template = '{0.username} - {0.model} - {0.ip_address} - {0.priv_address}'
        return template.format(self)
    
