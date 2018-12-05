from crontab import CronTab

cron = CronTab(user='ignatius')
job = cron.new(command='python3 /Users/andelae/python_dev/fly_airtech/manage.py send_flight_reminder',
               comment='send flight reminder email')
job.hour.every(1)

cron.write()
