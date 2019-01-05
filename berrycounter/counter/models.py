from django.db import models

# Create your models here.

COUNTER_CHOICES = (
    ('RW', 'Regenwater'),
    ('GAS', 'Gas'),
    ('DW', 'Stadswater'),
)

class Counter(models.Model):
    name = models.CharField(choices=COUNTER_CHOICES, max_length=100)
    pulses_today = models.IntegerField()
    pulses_this_hour = models.IntegerField()
    pulses_total = models.IntegerField()

    def __str__(self):
        return self.get_name_display()
