from crontab import CronTab
import datetime
import task_3 as t3
import time


ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
temp_cron = CronTab(user=True)
form = temp_cron.env['form']
env_file = temp_cron.env['env_file']
sys_data = t3.SystemData(st, env_file)
value = sys_data.collect_data()
t3.write_file('output', form, value)
