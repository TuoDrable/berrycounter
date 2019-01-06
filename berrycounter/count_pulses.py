import os
import django
import time
import random
import subprocess


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "berrycounter.settings")
django.setup()


from counter.models import Counter

DIRECTORY = './'

DEMO=False

if not DEMO:
    DIRECTORY = '/home/pi/rpi-sync/Berrycounter'

def to_RW_unit(pulse):
    return pulse


def to_GAS_unit(pulse):
    return pulse

def to_DW_unit(pulse):
    return pulse


def regenwater_pulse_seen():
    print ("RW pulse seen!")
    rw_object = Counter.objects.get(name='RW')
    rw_object.pulses_this_hour += 1
    rw_object.pulses_total += 1
    rw_object.pulses_today += 1
    rw_object.save()



def gas_pulse_seen():
    print ("GAS pulse seen!")
    gas_object = Counter.objects.get(name='GAS')
    gas_object.pulses_this_hour += 1
    gas_object.pulses_total +=1
    gas_object.pulses_today += 1
    gas_object.save()



def drinkwater_pulse_seen():
    print ("DW pulse seen!")
    dw_object = Counter.objects.get(name='DW')
    dw_object.pulses_this_hour += 1
    dw_object.pulses_total +=1
    dw_object.pulses_today += 1
    dw_object.save()


def create_file_if_not_existing_yet(filename, header):
    if not os.path.isfile(filename):
        with open(filename, 'w') as f:
            f.write(header + ";RW;GAS;DW")



def hour_has_passed(time_prev):
    print ("Hour has passed!")

    filename = DIRECTORY + 'pulsecounter_' + time.strftime("%d_%m_%Y", time_prev) + '.csv'

    create_file_if_not_existing_yet(filename, 'hour')

    with open(filename, 'a') as counterfile:
        counterfile.write('\n')
        counterfile.write(str(time_prev.tm_hour))
        counterfile.write(';')
        counterfile.write(str(to_RW_unit(Counter.objects.get(name='RW').pulses_this_hour)))
        counterfile.write(';')
        counterfile.write(str(to_GAS_unit(Counter.objects.get(name='GAS').pulses_this_hour)))
        counterfile.write(';')
        counterfile.write(str(to_DW_unit(Counter.objects.get(name='DW').pulses_this_hour)))

    for counter in Counter.objects.all():
        counter.pulses_this_hour = 0
        counter.save()

def day_has_passed(time_prev):
    print ("Day has passed!")

    filename = DIRECTORY + 'pulsecounter_' + time.strftime("%W_%Y", time_prev) + '.csv'

    create_file_if_not_existing_yet(filename, 'day')

    with open(filename, 'a') as counterfile:
        counterfile.write('\n')
        counterfile.write(time.strftime("%d-%m-%Y", time_prev))
        counterfile.write(';')
        counterfile.write(str(to_RW_unit(Counter.objects.get(name='RW').pulses_today)))
        counterfile.write(';')
        counterfile.write(str(to_GAS_unit(Counter.objects.get(name='GAS').pulses_today)))
        counterfile.write(';')
        counterfile.write(str(to_DW_unit(Counter.objects.get(name='DW').pulses_today)))


    for counter in Counter.objects.all():
        counter.pulses_today = 0
        counter.save()


def sync_with_dropbox():
    if not DEMO:
        subprocess.call("rclone sync /home/pi/rpi-sync/Berrycounter dropbox_brecht:Berrycounter/logging", shell=True)


if __name__=="__main__":
    print ("Start Counting! #counter = " + str(len(Counter.objects.all())))



    """
    # reset the counters at the beginning of the script
    for counter in Counter.objects.all():
        counter.pulses_today = 0
        counter.pulses_this_hour = 0
        counter.save()
    """

    time_prev = time.localtime()

    if DEMO:
        day_has_passed(time_prev)
    else:
        import RPi.GPIO as GPIO
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)

        # GPIO 23 & 17 & 24 set up as inputs, pulled up to avoid false detection.
        # So we'll be setting up falling edge detection for both
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(17, GPIO.FALLING, callback=regenwater_pulse_seen, bouncetime=50)
        GPIO.add_event_detect(23, GPIO.FALLING, callback=gas_pulse_seen, bouncetime=50)
        GPIO.add_event_detect(24, GPIO.FALLING, callback=drinkwater_pulse_seen, bouncetime=50)

    while True:
        time.sleep(1)
        now = time.localtime()

        if now.tm_hour != time_prev.tm_hour:
            hour_has_passed(time_prev)

        if now.tm_mday != time_prev.tm_mday:
            day_has_passed(time_prev)
            sync_with_dropbox()

        time_prev = now

        if DEMO:
            # create random pulses
            r = random.randrange(0, 10)
            if r < 3:
                regenwater_pulse_seen()

            if r >= 3 and r < 6:
                gas_pulse_seen()

            if r >= 6:
                drinkwater_pulse_seen()

