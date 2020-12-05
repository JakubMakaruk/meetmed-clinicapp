import datetime
theday = datetime.date.today()
weekday = theday.isoweekday()
print(theday)
print(weekday)

start = theday - datetime.timedelta(days=weekday)
print(start)

dates = [start + datetime.timedelta(days=d+1) for d in range(7)]

print(dates)