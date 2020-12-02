#!/usr/bin/python
from tracker import Tracker
import time
import schedule

TRACKING_INTERVAL = 15

tracker = Tracker()
tracker.run()
#schedule.every(TRACKING_INTERVAL).minute.do(tracker.run)
schedule.every(1).minute.do(tracker.run)
while True:
    schedule.run_pending()
    time.sleep(1)