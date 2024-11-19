from apscheduler.schedulers.blocking import BlockingScheduler
from app import generate_daily_python_question
from datetime import datetime

def daily_task():
    print(f"Running daily task at {datetime.now()}")
    generate_daily_python_question()

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # Schedule the task to run at midnight
    scheduler.add_job(daily_task, 'cron', hour=0, minute=0)
    print("Scheduler started. Waiting to run the task...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")