import hashlib,re,requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .config import settings
def clean(s):return re.sub(r"\\s+"," ",s or "").strip()
def fingerprint(s):return hashlib.sha256(clean(s).lower().encode()).hexdigest()
def category(t):
 t=t.lower();m=[("Recruitment",["recruitment","vacancy","job","bharti"]),("Result",["result","परिणाम"]),("Admit Card",["admit card","hall ticket"]),("Answer Key",["answer key"]),("Admission",["admission"]),("Scholarship",["scholarship","छात्रवृत्ति"]),("Examination",["exam","examination","परीक्षा"]),("Application Form",["application form","apply online"]),("Merit List",["merit list"]),("Counselling",["counselling","counseling"]),("Date Extension",["extension","extended"]),("Important Notice",["important notice","notice"]),("Certificate",["certificate"]),("Circular",["circular"])]
 for c,ks in m:
  if any(k in t for k in ks):return c
 return "Other"
def importance(t,k):
 return "HIGH" if any(x.strip().lower() in t.lower() for x in k.split(",") if x.strip()) else ("MEDIUM" if category(t)!="Other" else "LOW")
def fetch(u):
 r=requests.get(u,headers={"User-Agent":settings.user_agent},timeout=25);r.raise_for_status();return r.text,r.url
def scan_html(site):
 html,final=fetch(site.url);s=BeautifulSoup(html,"lxml");nodes=s.select(site.selector) if site.selector else [s.body or s];text=clean(" ".join(n.get_text(" ",strip=True) for n in nodes));out=[]
 for a in s.find_all("a",href=True):
  u=urljoin(final,a["href"]);t=clean(a.get_text(" ",strip=True)) or clean(u.rsplit("/",1)[-1].replace("-"," "))
  if len(t)<5:continue
  if any(x.strip().lower() in t.lower() for x in site.excluded_keywords.split(",") if x.strip()):continue
  out.append({"title":t[:500],"url":u,"content":text[:12000],"fingerprint":fingerprint(t+" "+text[:3000]),"category":category(t),"importance":importance(t,site.keywords)})
 return out[:100]
def scan_rss(site):
 import feedparser
 f=feedparser.parse(site.rss_url or site.url);return [{"title":clean(e.get("title","")),"url":e.get("link",site.url),"content":clean(BeautifulSoup(e.get("summary",""),"lxml").get_text(" ")),"fingerprint":fingerprint(e.get("title","")+e.get("summary","")),"category":category(e.get("title","")),"importance":importance(e.get("title",""),site.keywords)} for e in f.entries[:100]]
