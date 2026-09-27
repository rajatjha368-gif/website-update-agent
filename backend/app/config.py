import os
from dataclasses import dataclass
@dataclass
class Settings:
 database_url:str=os.getenv("DATABASE_URL","sqlite:///./data/agent.db"); secret_key:str=os.getenv("SECRET_KEY","change-me-in-production"); admin_username:str=os.getenv("ADMIN_USERNAME","admin"); admin_password:str=os.getenv("ADMIN_PASSWORD","change-me-now"); telegram_token:str=os.getenv("TELEGRAM_BOT_TOKEN",""); telegram_chat_id:str=os.getenv("TELEGRAM_CHAT_ID",""); smtp_host:str=os.getenv("SMTP_HOST",""); smtp_port:int=int(os.getenv("SMTP_PORT","587")); smtp_username:str=os.getenv("SMTP_USERNAME",""); smtp_password:str=os.getenv("SMTP_PASSWORD",""); email_from:str=os.getenv("EMAIL_FROM",""); email_to:str=os.getenv("EMAIL_TO",""); user_agent:str=os.getenv("USER_AGENT","WebsiteUpdateAgent/1.0 (+monitor)")
settings=Settings()
