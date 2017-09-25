from apscheduler.schedulers.blocking import BlockingScheduler
import time
import datetime

sched = BlockingScheduler()

def timestamp_to_datetime(unix_time: int, date_format='%Y-%m-%d %H:%M:%S') -> str:
    if isinstance(unix_time, int):
        output = datetime.datetime.fromtimestamp(unix_time).strftime(date_format)

    elif isinstance(unix_time, str):
        output = datetime.datetime.fromtimestamp(int(unix_time)).strftime(date_format)

    else:
        output = '0000-00-00 00:00:00'

    return output


@sched.scheduled_job('interval', seconds=1)
def timed_job():
    unix_time = int(time.time())
    print(timestamp_to_datetime(unix_time))

sched.start()
