from pydantic import BaseModel,AnyHttpUrl,Field
class Login(BaseModel): username:str; password:str
class WebsiteIn(BaseModel): name:str; url:AnyHttpUrl; monitor_type:str="html"; enabled:bool=True; interval:int=Field(30,ge=1); priority:str="MEDIUM"; keywords:str=""; excluded_keywords:str=""; selector:str=""; rss_url:str=""; js_render:bool=False; pdf_monitor:bool=True; notify_telegram:bool=True; notify_email:bool=False
