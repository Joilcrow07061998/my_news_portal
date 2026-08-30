from apscheduler.schedulers.background import BackgroundScheduler

from .tasks import send_weekly_newsletter


def start():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        send_weekly_newsletter,
        'interval',
        weeks=1,
        id='weekly_newsletter',
        replace_existing=True,
    )

    scheduler.start()