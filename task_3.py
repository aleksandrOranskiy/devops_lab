from crontab import CronTab
import json
import psutil


class ConfigFile(object):
    """Class for parsing configuration files"""
    def __init__(self, filename):
        self.filename = filename
        self.result_list = []

    def parse_file(self):

        try:
            with open(self.filename) as f:

                # receiving and checking value from the first line
                main_value = f.readline().strip()
                if main_value != "[common]":
                    print("An invalid value in the first line!")
                    return 1
                else:
                    self.result_list.append(main_value)

                # receiving and checking value from the second line
                output_value = f.readline().strip().split()
                if output_value[0] != "output":
                    print("The second line should start with 'output'")
                    return 1
                elif output_value[2] != "json" and output_value[2] != "plain":
                    print("A value in the second line should be (json|plain)")
                    return 1
                else:
                    self.result_list.append(output_value[2])

                # receiving and checking value from the third line
                interval_value = f.readline().strip().split()
                if interval_value[0] != "interval":
                    print("The third line should start with 'interval'")
                    return 1
                else:
                    try:
                        interval = int(interval_value[2])
                    except ValueError:
                        print("The number in the third line isn't correct")
                        return 1
                    else:
                        self.result_list.append(interval)

                # receiving and checking value from the fourth line
                    env_file = f.readline().strip().split()
                    if env_file[0] != "env_file":
                        print("The fourth line should start with 'env_file'")
                        return 1
                    elif env_file[2]:
                        self.result_list.append(env_file[2])
                    else:
                        self.result_list.append("env")

                # receiving and checking value from the fifth line
                    python_path = f.readline().strip().split()
                    if python_path[0] != "python_path":
                        print("The fifth line should start with 'python_path'")
                        return 1
                    elif python_path[2]:
                        self.result_list.append(python_path[2])
                    else:
                        self.result_list.append("$(which python)")

                # receiving and checking value from the sixth line
                    script_path = f.readline().strip().split()
                    if script_path[0] != "script_path":
                        print("The sixth line should start with 'script_path'")
                        return 1
                    elif script_path[2]:
                        self.result_list.append(script_path[2])
                    else:
                        self.result_list.append("cron.py")

        except IOError:
            print("File doesn't exist")


class SystemData(object):
    """Class for collecting a system information"""
    def __init__(self, timestamp, env_file):
        self.network_if = list(psutil.net_if_stats().keys())[0]
        self.cpu = {
            "cpu_iowait": psutil.cpu_times()[4],
            "cpu_percent": psutil.cpu_percent(interval=None),
            "cpu_count": psutil.cpu_count(),
            "cpu_interrupts": psutil.cpu_stats()[1],
            "cpu_frequency": psutil.cpu_freq()[0]
        }
        self.vm = {
            "virtual_memory_free": psutil.virtual_memory()[4],
            "swap_memory_free": psutil.swap_memory()[2]
        }
        self.memory = {
            "disk_free": psutil.disk_usage('/')[2]
        }
        self.io = {
            "disk_read": psutil.disk_io_counters()[0],
            "disk_write": psutil.disk_io_counters()[1]
        }
        self.network = {
            "net_bytes_sent": psutil.net_io_counters()[0],
            "net_bytes_recv": psutil.net_io_counters()[1],
            "net_address": psutil.net_if_addrs()[self.network_if][0][1],
            "net_mask": psutil.net_if_addrs()[self.network_if][0][2]
        }
        self.timestamp = timestamp
        self.env_file = env_file
        self.index = 0

    def __str__(self):
        return "SNAPSHOT {0}".format(self.index)

    def get_index(self):
        try:
            with open(self.env_file) as infile:
                self.index = int(infile.readline())
        except IOError:
            print("File doesn't exist")

    def set_env(self):
        self.index += 1
        with open(self.env_file, 'w') as outfile:
            outfile.write(str(self.index))

    def collect_data(self):
        self.get_index()
        result_data = {
            str(self): self.timestamp,
            "cpu": self.cpu,
            "vm": self.vm,
            "memory": self.memory,
            "io": self.io,
            "network": self.network
        }
        self.set_env()

        return result_data


def write_file(filename, form, data):

    try:
        with open(filename, 'a') as outfile:
            if form == "json":
                json.dump(data, outfile)
            elif form == "plain":
                counter = 0
                for K, V in data.items():
                    if counter == 0:
                        outfile.write("\n" + " " + K + " : " + V)
                        counter += 1
                        continue
                    else:
                        outfile.write(" " + K + " < ")
                    for k, v in data[K].items():
                        if counter == 1:
                            outfile.write(str(k) + " : " + str(v))
                            counter += 1
                        else:
                            outfile.write(", " + str(k) + " : " + str(v))
                    outfile.write(" >")
            else:
                print("Unknown format")
                return 1
            outfile.write("\n")
    except IOError:
        print("File doesn't exist")


def cron_schedule(interval, form, env_file, python_path, script_path):

    system_cron = CronTab(user=True)
    job = system_cron.new(command=python_path + " " + script_path)
    job.minute.every(interval)
    system_cron.env['form'] = form
    system_cron.env['env_file'] = env_file
    job.enable()
    system_cron.write_to_user(user=True)

    return job
