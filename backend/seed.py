from app.database import Base,engine,SessionLocal
from app.models import Website
Base.metadata.create_all(bind=engine)
sites=[("LNMU","https://lnmu.ac.in/"),("BSEB Bihar","https://secondary.biharboardonline.com/"),("Bihar Raj Bhavan","https://governor.bih.nic.in/"),("MedhaSoft Bihar","https://medhasoft.bih.nic.in/"),("Bihar PMS","https://pmsonline.bihar.gov.in/"),("NSP","https://scholarships.gov.in/"),("Sarkari Result","https://www.sarkariresult.com/"),("BPSC","https://bpsc.bihar.gov.in/"),("UPSC","https://upsc.gov.in/"),("SSC","https://ssc.gov.in/")]
d=SessionLocal()
for n,u in sites:
 if not d.query(Website).filter(Website.url==u).first():d.add(Website(name=n,url=u,priority="HIGH",keywords="result,admit card,answer key,recruitment,notification,exam,scholarship,application,deadline"))
d.commit();d.close()
