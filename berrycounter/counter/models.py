from django.db import models

# Create your models here.

COUNTER_CHOICES = (
    ('RW', 'Regenwater'),
    ('GAS', 'Gas'),
    ('DW', 'Stadswater'),
)

UNIT_CHOICES = (
    ('m3/h', 'kubiek'),
    ('kWh', 'kilowattuur'),
)

class Counter(models.Model):
    name = models.CharField(choices=COUNTER_CHOICES, max_length=100)
    pulses_today = models.IntegerField()
    pulses_this_hour = models.IntegerField()
    pulses_total = models.IntegerField()

    unit = models.CharField(choices=UNIT_CHOICES, max_length=100, default='m3/h')
    conversion_multiplier = models.FloatField(default=1)

    def __str__(self):
        return self.get_name_display()

class DayHistory(models.Model):
    counter = models.ForeignKey(Counter, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    hour = models.IntegerField()
    value = models.IntegerField()

    def __str__(self):
        return str(counter) + ' | ' + str(date) + ' ' + hour + ':00 | ' + value + ' pulses'

class WeekHistory(models.Model):
    counter = models.ForeignKey(Counter, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    week = models.IntegerField()
    value = models.IntegerField()

    def __str__(self):
        return str(counter) + ' | week ' + str(week) + ' - ' + str(date) + ' | ' + value + ' pulses'

