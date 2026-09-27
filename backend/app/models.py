from sqlalchemy import Column,Integer,String,Boolean,Text,DateTime,ForeignKey
from datetime import datetime
from .database import Base
class Website(Base):
 __tablename__="websites"; id=Column(Integer,primary_key=True); name=Column(String(200),nullable=False); url=Column(String(1000),nullable=False); monitor_type=Column(String(30),default="html"); enabled=Column(Boolean,default=True); interval=Column(Integer,default=30); priority=Column(String(20),default="MEDIUM"); keywords=Column(Text,default=""); excluded_keywords=Column(Text,default=""); selector=Column(Text,default=""); rss_url=Column(String(1000),default=""); js_render=Column(Boolean,default=False); pdf_monitor=Column(Boolean,default=True); notify_telegram=Column(Boolean,default=True); notify_email=Column(Boolean,default=False); created_at=Column(DateTime,default=datetime.utcnow)
class Update(Base):
 __tablename__="updates"; id=Column(Integer,primary_key=True); website_id=Column(Integer,ForeignKey("websites.id"),index=True); title=Column(String(500)); url=Column(String(1500)); category=Column(String(80)); importance=Column(String(20)); summary=Column(Text); content=Column(Text); fingerprint=Column(String(64),index=True); status=Column(String(20)); published_date=Column(String(100)); important_date=Column(String(100)); pdf_url=Column(String(1500)); created_at=Column(DateTime,default=datetime.utcnow,index=True)
class Scan(Base):
 __tablename__="scans"; id=Column(Integer,primary_key=True); website_id=Column(Integer,ForeignKey("websites.id")); status=Column(String(20)); message=Column(Text); started_at=Column(DateTime,default=datetime.utcnow); finished_at=Column(DateTime)
