from crontab import CronTab
import datetime
import task_3 as t3
import time


ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
sys_data = t3.SystemData(st)
value = sys_data.collect_data()
temp_cron = CronTab(user='student')
form = temp_cron.env['form']
t3.write_file('/home/student/PycharmProjects/task_3/output', form, value)
