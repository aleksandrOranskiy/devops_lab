import task_3 as t3


config_file = t3.ConfigFile('/home/student/PycharmProjects/task_3/config.ini')
config_file.parse_file()
config_values = config_file.result_list
interval = config_values[2]
form = config_values[1]
t3.cron_schedule(interval, form)
