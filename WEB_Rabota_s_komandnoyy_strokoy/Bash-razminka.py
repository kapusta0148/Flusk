import schedule
import time
from datetime import datetime

def ku_job():
    current_hour = datetime.now().hour
    repeat_count = current_hour % 12
    repeat_count = 12 if repeat_count == 0 else repeat_count
    print("Ку " * repeat_count)

schedule.every().hour.at(":00").do(ku_job)

while True:
    schedule.run_pending()
    time.sleep(1)