from backend.app.monitors import fingerprint,category,importance
def test_fingerprint_stable():assert fingerprint("ABC")==fingerprint("ABC")
def test_category():assert category("Admit Card 2026")=="Admit Card"
def test_importance():assert importance("Recruitment Notification","recruitment")=="HIGH"
