from apscheduler.schedulers.background import BackgroundScheduler
from .database import SessionLocal
from .models import Website
scheduler=BackgroundScheduler()
def schedule_site(w):
 from .api import do_scan
 scheduler.add_job(do_scan,"interval",minutes=max(1,w.interval),args=[w.id],id=f"site-{w.id}",replace_existing=True)
def unschedule_site(id):
 try:scheduler.remove_job(f"site-{id}")
 except Exception:pass
def start_scheduler():
 if scheduler.running:return
 d=SessionLocal()
 for w in d.query(Website).filter(Website.enabled==True).all():schedule_site(w)
 d.close();scheduler.start()
