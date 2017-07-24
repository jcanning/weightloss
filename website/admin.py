from django.contrib import admin
from .models import *
from .forms import *

admin.site.register({Members,Payments})
