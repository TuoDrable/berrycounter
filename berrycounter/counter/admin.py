from django.contrib import admin

# Register your models here.

from .models import *


@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = ('name', 'pulses_this_hour', 'pulses_today', 'pulses_total')

@admin.register(DayHistory)
class DayHistoryAdmin(admin.ModelAdmin):
    list_display = ('counter', 'date', 'hour', 'value')

@admin.register(WeekHistory)
class WeekHistoryAdmin(admin.ModelAdmin):
    list_display = ('counter', 'week', 'date', 'value')
