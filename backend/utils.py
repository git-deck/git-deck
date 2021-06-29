import datetime


def days_hours_minutes_seconds(td):
	return td.days, td.seconds//3600, (td.seconds//60)%60, td.seconds%60


def how_long_ago(time):
	now = datetime.datetime.now()
	td = now - time
	days, hours, minutes, seconds = days_hours_minutes_seconds(td)
	if time.year != now.year:
		return time.strftime("%d %b %Y")
	if days >= 7:
		return time.strftime("%b %d")
	if days > 0:
		return "{}d".format(days)
	if td.seconds >= 60*60:
		return "{}h".format(hours)
	if td.seconds >= 60:
		return "{}m".format(minutes)
	return "{}s".format(seconds)
