from datetime import datetime,timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException,Depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from .config import settings
pwd=CryptContext(schemes=["bcrypt"],deprecated="auto"); bearer=HTTPBearer()
def token(username): return jwt.encode({"sub":username,"exp":datetime.utcnow()+timedelta(hours=12)},settings.secret_key,algorithm="HS256")
def verify(username,password): return username==settings.admin_username and pwd.verify(password,pwd.hash(settings.admin_password))
def require_auth(c:HTTPAuthorizationCredentials=Depends(bearer)):
 try:return jwt.decode(c.credentials,settings.secret_key,algorithms=["HS256"])["sub"]
 except Exception:raise HTTPException(401,"Invalid or expired token")
