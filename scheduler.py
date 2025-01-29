import schedule
import time
import sync_grocy

def sync():
    sync_grocy.main()

def run():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__=="__main__":
    sync()
    schedule.every(15).minutes.do(sync)
    run()