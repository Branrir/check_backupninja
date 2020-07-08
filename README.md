# Nagios Backupninja check

Nagios Check for Backupninja. This check monitors logs for errors.

## For Python requirements run:

sudo pip3 install -r requirements

## Installation:

```bash
cd /usr/lib/nagios/plugins
wget https://raw.githubusercontent.com/Branrir/check_backupninja/master/check_backupninja.py
chmod +x check_bandwidth.py
```
## 

| Parameter | Description |
| --- | --- |
| -h, --help | Shows help |
| -w, --warning | Warning value in days |
| -c, --critical | Critical value in days |
| -l, --log | Log file location. Default /var/log/backupninja.log |

Example usage:
```bash
/usr/lib/nagios/plugins/check_backupninja.py -c 10 -w 5 -l /var/log/custom/backup.log
```
Output: 
```bash
OK - Last Backup: 2020-07-08 02:53:32
```

-------
ToDo

* Better way to parse logs (multiple backups support)
