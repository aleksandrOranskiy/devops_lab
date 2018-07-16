import task_3 as t3


config_file = t3.ConfigFile('config.ini')
config_file.parse_file()
config_values = config_file.result_list
interval = config_values[2]
form = config_values[1]
env_file = config_values[3]
python_path = config_values[4]
script_path = config_values[5]
t3.cron_schedule(interval, form, env_file, python_path, script_path)
