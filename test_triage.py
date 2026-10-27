import triage

def test_classify1():
    assert triage.classify("VPN", "impossible de me connecter au vpn depuis chez moi") == "Network"
    
def test_classify2():
    assert triage.classify("Excel", "excel plante sur le réseau de l'entreprise") == "Need_review"    
   
def test_classify3():
    assert triage.classify("Aide", "Help") == "Need_review"    