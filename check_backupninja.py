#!/usr/bin/python3
import argparse
import sys
import re
import datetime

# Return codes
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3


def main(args):
    states = []
    tmp_str = ''
    backup_date = "never"

    try:
        with open(args.log, "r") as file:
            for line in file:
                if "FINISHED" in line:
                    date = re.search(r"\w{3}\s\d{2}\s\d{2}\:\d{2}\:\d{2}", line).group()
                    backup_date = datetime.datetime.strptime(date, '%b %d %H:%M:%S')
                    backup_date = backup_date.replace(year=datetime.datetime.now().year)
                    backup_warn = backup_date + datetime.timedelta(days=int(args.warning))
                    backup_crit = backup_date + datetime.timedelta(days=int(args.critical))
                    tmp = line.rsplit(' ', 6)
                    warning = tmp[-2]
                    error = tmp[-4]
                    fatal = tmp[-6]
                    if datetime.datetime.now() >= backup_crit and error == 0 and warning == 0 and fatal == 0:
                        tmp_str += 'Last Backup: {0}'.format(backup_date)
                        states.append(CRITICAL)
                    if datetime.datetime.now() >= backup_warn and error == 0 and warning == 0 and fatal == 0:
                        tmp_str += 'Last Backup: {0}'.format(backup_date)
                        states.append(WARNING)
                    if (error != 0 or fatal != 0) and warning == 0:
                        tmp_str += 'Last Backup: {0} finished with {1} fatals and {2} errors'.format(backup_date, fatal,
                                                                                                     error)
                        states.append(CRITICAL)
                    if error == 0 and fatal == 0 and warning != 0:
                        tmp_str += 'Last Backup: {0} finished with {1} warnings'.format(backup_date, warning)
                        states.append(WARNING)
    except Exception as e:
        print('Cannot open logs: {0}'.format(e))
        sys.exit(UNKNOWN)

    # Check states
    if CRITICAL in states:
        print('CRITICAL - ' + tmp_str)
        sys.exit(CRITICAL)
    if WARNING in states and CRITICAL not in states:
        print('WARNING - ' + tmp_str)
        sys.exit(WARNING)
    if CRITICAL not in states and WARNING not in states and WARNING not in states:
        print('OK - Last Backup: {0}'.format(backup_date))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--critical', help='Number of days without backup (Critical)')
    parser.add_argument('-w', '--warning', help='Number of days without backup (Warning)')
    parser.add_argument('-l', '--log', help='Location of Backupninja log', default='/var/log/backupninja.log')
    args = parser.parse_args()
    main(args)
