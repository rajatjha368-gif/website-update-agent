import hashlib,requests
from io import BytesIO
try:
 from pypdf import PdfReader
except ImportError: PdfReader=None
from .config import settings
from .monitors import clean,category,importance
def scan_pdf(site):
 r=requests.get(site.url,headers={"User-Agent":settings.user_agent},timeout=30);r.raise_for_status()
 data=r.content; text=""
 if PdfReader:
  reader=PdfReader(BytesIO(data));text=clean("\n".join((p.extract_text() or "") for p in reader.pages))
 fp=hashlib.sha256(data).hexdigest()
 title=site.name+" PDF"
 return [{"title":title,"url":r.url,"content":text[:20000],"fingerprint":fp,"category":category(title+" "+text[:500]),"importance":importance(title+" "+text[:500],site.keywords)}]
