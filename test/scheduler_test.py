import importer_test
import schedule
import time
from schedulers.pingSchedule import pingServerJob, pingDbJob, toThread
import concurrent.futures


pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)

# schedule.every(1).minutes.do(pingServerJob)
# schedule.every(1).minutes.do(pingDbJob)


# def toThread():
#     pool.submit(pingServerJob)
#     pool.submit(pingDbJob)
    # pool.shutdown(wait=True)


schedule.every(10).seconds.do(toThread)


def main():
    print("Scheduler started")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
