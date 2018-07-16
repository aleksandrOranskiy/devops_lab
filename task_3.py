from crontab import CronTab
import json
import psutil


def parse_file(filename):

    result_list = []
    try:
        with open(filename) as f:

            # receiving and checking value from the first line
            main_value = f.readline().strip()
            if main_value != "[common]":
                print("An invalid value in the first line!")
                return 1
            else:
                result_list.append(main_value)

            # receiving and checking value from the second line
            output_value = f.readline().strip().split()
            if output_value[0] != "output":
                print("The second line should start with 'output'")
                return 1
            elif output_value[2] != "json" and output_value[2] != "plain":
                print("A value in the second line should be (json|plain)")
                return 1
            else:
                result_list.append(output_value[2])

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
                    result_list.append(interval)
    except IOError:
        print("File doesn't exist")

    return result_list


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


def collect_system_data(timestamp):

    try:
        with open('env', 'r') as infile:
            index = temp = int(infile.readline())
    except IOError:
        print("File doesn't exist")
        index = temp = 1

    temp += 1
    with open('env', 'w') as outfile:
        outfile.write(str(temp))
    net_if = list(psutil.net_if_stats().keys())[0]
    result_data = {
        "SNAPSHOT {0}".format(index): timestamp,
        "cpu": {
            "cpu_iowait": psutil.cpu_times()[4],
            "cpu_percent": psutil.cpu_percent(interval=None),
            "cpu_count": psutil.cpu_count(),
            "cpu_interrupts": psutil.cpu_stats()[1],
            "cpu_frequency": psutil.cpu_freq()[0]
        },
        "vm": {
            "virtual_memory_free": psutil.virtual_memory()[4],
            "swap_memory_free": psutil.swap_memory()[2]
        },
        "memory": {
            "disk_free": psutil.disk_usage('/')[2]
        },
        "io": {
            "disk_read": psutil.disk_io_counters()[0],
            "disk_write": psutil.disk_io_counters()[1]
        },
        "network": {
            "net_bytes_sent": psutil.net_io_counters()[0],
            "net_bytes_recv": psutil.net_io_counters()[1],
            "net_address": psutil.net_if_addrs()[net_if][0][1],
            "net_mask": psutil.net_if_addrs()[net_if][0][2]
        }
    }

    return result_data


def cron_schedule(interval, form):

    system_cron = CronTab(user=True)
    job = system_cron.new(command='/home/student/.pyenv/versions'
                                  '/3.7.0/bin/python '
                                  '/home/student/devops_lab/cron.py')
    job.minute.every(interval)
    system_cron.env['form'] = form
    job.enable()
    system_cron.write_to_user(user=True)

    return job
