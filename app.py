import schedule
import time
from modules.pingSchedule import job


def main():
    print("Starting...")

schedule.every(5).seconds.do(job)

if __name__ == '__main__':
    main()
    while True:
        schedule.run_pending()
        time.sleep(1)