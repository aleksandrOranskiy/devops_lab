import task_3 as t3


config_file = '/home/student/PycharmProjects/task_3/config.ini'
config_values = t3.parse_file(config_file)
interval = config_values[2]
form = config_values[1]
t3.cron_schedule(interval, form)
