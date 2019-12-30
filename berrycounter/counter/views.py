from django.shortcuts import render
from datetime import datetime, timedelta
from collections import defaultdict

from .models import DayHistory

def index(request):
    dataset = DayHistory.objects.filter(date__gte=datetime.now()-timedelta(days=30)).order_by('date')
    days = []
    counters = defaultdict(list)
    for dayhistory in dataset:
        if dayhistory.date not in days:
            days.append(dayhistory.date)
        
        counters[dayhistory.counter.name].append(dayhistory.value)

    dataset = DayHistory.objects.filter(date__year=datetime.now().year).order_by('date')

    months = []
    month_counters = defaultdict(list)

    month_tally = defaultdict(int)
    for dayhistory in dataset:
        if dayhistory.date.month not in months:
            months.append(dayhistory.date.month)
            for name, value in month_tally.items():
                month_counters[name].append(value)
            month_tally = defaultdict(int)

        month_tally[dayhistory.counter.name] += dayhistory.value

    for name, value in month_tally.items():
        month_counters[name].append(value)
        month_tally = defaultdict(int)

    return render(request, 'counter/index.html', {'counters': dict(counters), 'days': days, 'months': months, 'month_counters': dict(month_counters)})
