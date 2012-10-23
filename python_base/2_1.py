#! /usr/bin env python
#根据给定的年月日以数字的形式打印日期
#2012-10-23  XXG

months = [
	'Jan',
	'Feb',
	'Mar',
	'Apr',
	'May',
	'Jun',
	'Jul',
	'Aug',
	'Sep',
	'Oct',
	'Nov',
	'Dec'
	]

endings = ['st','nd','rd'] + 17 * ['th'] \
        + ['st','nd','rd'] + 7  * ['th'] \
        + ['st']

year  = raw_input("year:")
month = raw_input("month(1-12):")
day   = raw_input("day(1-31):")

month_number = int(month)
day_number   = int(day)

month_name = months[month_number - 1]
ordinal    = day + endings[day_number - 1]

print month_name + ' ' + ordinal + '.' + year
