from .monitors import scan_html
def scan_playwright(site):
 try:
  from playwright.sync_api import sync_playwright
 except ImportError: return scan_html(site)
 with sync_playwright() as p:
  b=p.chromium.launch(headless=True);page=b.new_page();page.goto(site.url,wait_until="networkidle",timeout=30000)
  html=page.content();b.close()
 from bs4 import BeautifulSoup
 s=BeautifulSoup(html,"lxml")
 return [{"title":site.name,"url":site.url,"content":s.get_text(" ",strip=True)[:12000],"fingerprint":__import__("hashlib").sha256(s.get_text(" ",strip=True).encode()).hexdigest(),"category":"Other","importance":"MEDIUM"}]
