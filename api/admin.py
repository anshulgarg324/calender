from django.contrib import admin
# from django.forms import CheckboxSelectMultiple
from django.db import models
# Register your models here.

from .models import *

admin.site.register(GoogleData)
admin.site.register(Event)