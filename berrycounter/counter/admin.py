from django.contrib import admin

# Register your models here.

from .models import Counter


@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = ('name', 'pulses_this_hour', 'pulses_today', 'pulses_total')
