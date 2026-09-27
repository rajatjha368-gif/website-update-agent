from apscheduler.schedulers.background import BackgroundScheduler
from .database import SessionLocal
from .models import Website
from .api import do_scan
scheduler=BackgroundScheduler()
def start_scheduler():
 if scheduler.running:return
 d=SessionLocal()
 for w in d.query(Website).filter(Website.enabled==True).all():scheduler.add_job(do_scan,"interval",minutes=max(1,w.interval),args=[w.id],id=f"site-{w.id}",replace_existing=True)
 d.close();scheduler.start()
