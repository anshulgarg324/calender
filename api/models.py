"""
This contains the database architecture and all the field
listed in the tables field

"""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date
import datetime

class Event(models.Model):
    """
    This class contains the database architecture and all the field
    listed in the event tables

    """
    user = models.ForeignKey(User)
    location = models.CharField(max_length=50, blank=True, null=True)
    google_id = models.CharField(max_length=50, blank=True, null=True,
                                unique=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    all_day = models.BooleanField(default=False)
    is_updated = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        """
        This method checks the below conndition before populating
        database

        """
        if self.start_date > self.end_date:
            raise ValueError('Start Date should be less than End Date')
        else:
            super(Event, self).save()

class GoogleData(models.Model):
    """
    This class contains the database architecture and all the field
    listed from the googles data

    """
    user = models.OneToOneField(User)
    last_sync = models.DateTimeField(blank=True, null=True)
    refresh_token = models.CharField(max_length=256, null=True, blank=True)
    def __str__(self):
        return self.user.username

