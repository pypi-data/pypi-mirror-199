from crontab import CronTab


def start_daemon():
    cron = CronTab(user="ubuntu")
    for _job in cron:
        if _job.comment == "daemon":
            return
    job = cron.new(
        command="/home/ubuntu/python/queue_tel_bot/.venv/bin/python /home/ubuntu/python/queue_tel_bot/queue_bot/base/klient.py",
        comment="daemon",
    )
    job.minute.every(1)
    cron.write()


def close_daemon():
    cron = CronTab(user="ubuntu")
    for job in cron:
        if job.comment == "daemon":
            cron.remove(job)
            cron.write()
