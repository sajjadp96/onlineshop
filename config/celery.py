from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Tehran')

app.autodiscover_tasks()



app.conf.beat_schedule = {
    'send-ad-mail-every-day': {
        'task': 'user.tasks.send_ad_mails',
        'schedule':crontab(hour=21, minute=15),
        # 'args' : ("I am crazy saji.",)
    }
}