import requests,smtplib
from email.mime.text import MIMEText
from .config import settings
def message(u,site):return f"🔔 {site.name}\n\n{u.title}\nCategory: {u.category}\nImportance: {u.importance}\n\n{u.summary[:700]}\n\nOfficial link: {u.url}"
def telegram(u,site):
 if not settings.telegram_token or not settings.telegram_chat_id:return
 requests.post(f"https://api.telegram.org/bot{settings.telegram_token}/sendMessage",json={"chat_id":settings.telegram_chat_id,"text":message(u,site)},timeout=15)
def email(u,site):
 if not settings.smtp_host or not settings.email_to:return
 m=MIMEText(message(u,site));m["Subject"]=f"[{u.importance}] {u.title}";m["From"]=settings.email_from;m["To"]=settings.email_to
 with smtplib.SMTP(settings.smtp_host,settings.smtp_port,timeout=20) as s:s.starttls();s.login(settings.smtp_username,settings.smtp_password);s.send_message(m)
