from django.contrib import admin
from .models import *
from .forms import *

@admin.register(Weighins)
class WeighinsAdmin(admin.ModelAdmin):
    list_display = ('member','date','weight')
    ordering = ('member','date')

@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('member','date','amount')
    ordering = ('member','date')

admin.site.register({Members,})
