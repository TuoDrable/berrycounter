import os
import django
import time
from datetime import datetime
import random
import subprocess


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "berrycounter.settings")
django.setup()


from counter.models import *

DIRECTORY = './'

DEMO=False

if not DEMO:
    DIRECTORY = '/home/pi/berry-stats/'


def parse_file(file):
    lines = file.readlines()
    if 'day' in lines[0]:
        for line in lines[1:]:
            print(line)
            line_splitted = line.split(';')
            dt = datetime.strptime(line_splitted[0], '%d-%m-%Y')
            gas = int(float(line_splitted[2]))

            print("date:", dt.date(), "gas", gas)
            gas_entry = DayHistory.objects.create(counter=Counter.objects.get(name='GAS'), date=dt.date(), weekday=dt.weekday(), value=gas)
            gas_entry.save()



if __name__ == '__main__':
    for filename in os.listdir(DIRECTORY):
        with open(os.path.join(DIRECTORY, filename)) as file:
            parse_file(file)
