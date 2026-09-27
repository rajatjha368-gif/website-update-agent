from fastapi import APIRouter,Depends,HTTPException,BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
from .database import SessionLocal
from .models import Website,Update,Scan
from .schemas import Login,WebsiteIn
from .auth import token,verify,require_auth
from .monitors import scan_html,scan_rss
from .notifications import telegram,email
router=APIRouter()
def db():
 d=SessionLocal()
 try:yield d
 finally:d.close()
@router.post("/auth/login")
def login(x:Login):
 if not verify(x.username,x.password):raise HTTPException(401,"Invalid credentials")
 return {"access_token":token(x.username),"token_type":"bearer"}
@router.get("/stats")
def stats(d:Session=Depends(db),_=Depends(require_auth)):return {"websites":d.query(Website).count(),"updates":d.query(Update).count(),"scans":d.query(Scan).count(),"high_priority":d.query(Update).filter(Update.importance=="HIGH").count()}
@router.get("/websites")
def websites(d:Session=Depends(db),_=Depends(require_auth)):return d.query(Website).order_by(Website.id.desc()).all()
@router.post("/websites")
def add(x:WebsiteIn,d:Session=Depends(db),_=Depends(require_auth)):
 w=Website(**x.model_dump());d.add(w);d.commit();d.refresh(w)
 from .scheduler import schedule_site
 if w.enabled:schedule_site(w)
 return w
@router.put("/websites/{id}")
def edit(id:int,x:WebsiteIn,d:Session=Depends(db),_=Depends(require_auth)):
 w=d.get(Website,id)
 if not w:raise HTTPException(404,"Website not found")
 for k,v in x.model_dump().items():setattr(w,k,v)
 d.commit()
 from .scheduler import schedule_site,unschedule_site
 if w.enabled:schedule_site(w)
 else:unschedule_site(w.id)
 return w
@router.delete("/websites/{id}")
def delete(id:int,d:Session=Depends(db),_=Depends(require_auth)):
 w=d.get(Website,id)
 if not w:raise HTTPException(404,"Website not found")
 from .scheduler import unschedule_site
 unschedule_site(id);d.delete(w);d.commit();return {"ok":True}
def do_scan(id):
 d=SessionLocal();w=d.get(Website,id);s=Scan(website_id=id,status="RUNNING");d.add(s);d.commit()
 try:
  items=scan_rss(w) if w.monitor_type=="rss" else scan_html(w);n=0
  for x in items:
   if d.query(Update).filter(Update.fingerprint==x["fingerprint"]).first():continue
   u=Update(website_id=id,title=x["title"],url=x["url"],category=x["category"],importance=x["importance"],summary=x["content"][:1000],content=x["content"],fingerprint=x["fingerprint"],status="NEW");d.add(u);d.commit();n+=1
   try:
    if w.notify_telegram:telegram(u,w)
    if w.notify_email:email(u,w)
   except Exception:pass
  s.status="SUCCESS";s.message=f"{n} new updates"
 except Exception as e:s.status="FAILED";s.message=str(e)
 s.finished_at=datetime.utcnow();d.commit();d.close()
@router.post("/websites/{id}/scan")
def scan(id:int,bg:BackgroundTasks,d:Session=Depends(db),_=Depends(require_auth)):
 if not d.get(Website,id):raise HTTPException(404,"Website not found")
 bg.add_task(do_scan,id);return {"queued":True}
@router.get("/updates")
def updates(limit:int=100,d:Session=Depends(db),_=Depends(require_auth)):return d.query(Update).order_by(Update.created_at.desc()).limit(limit).all()
@router.get("/scans")
def scans(limit:int=100,d:Session=Depends(db),_=Depends(require_auth)):return d.query(Scan).order_by(Scan.started_at.desc()).limit(limit).all()
