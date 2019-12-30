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

class HourHistory(models.Model):
    counter = models.ForeignKey(Counter, on_delete=models.CASCADE)
    date = models.DateField()
    hour = models.IntegerField()
    value = models.IntegerField()

    def __str__(self):
        return str(self.counter) + ' | ' + str(self.date) + ' ' + str(self.hour) + ':00 | ' + str(self.value) + ' pulses'

class DayHistory(models.Model):
    counter = models.ForeignKey(Counter, on_delete=models.CASCADE)
    date = models.DateField()
    weekday = models.IntegerField()
    value = models.IntegerField()

    def __str__(self):
        return str(self.counter) + ' | week ' + str(self.weekday) + ' - ' + str(self.date) + ' | ' + str(self.value) + ' pulses'

