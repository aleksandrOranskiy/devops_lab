from crontab import CronTab
import datetime
import task_3 as t3
import time


ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
value = t3.collect_system_data(st)
temp_cron = CronTab(user='student')
form = temp_cron.env['form']
t3.write_file('/home/student/PycharmProjects/task_3/output', form, value)
