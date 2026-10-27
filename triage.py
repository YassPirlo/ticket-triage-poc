import csv
import genai
        
        
KEYWORDS  = {
    "Network" : ["réseau", "vpn", "wifi", "5g", "internet"],
    "Hardware": ["imprimante", "ventillateur", "chauffe", "souris", "clavier", "ecran", "ordinateur","laptop"],
    "Software": ["software", "application", "programme", "installer", "mise à jour", "update","excel"],
    "Security": ["security", "virus", "malware", "phishing"],
    "Access": ["compte", "login", "password", "credentials", "authentification", "authentifier", "connexion","accès", "autorisation", "permission"],
    "Email": ["email", "mail", "messagerie", "smtp", "imap", "outlook", "gmail", "hotmail"],
    }    

#print(KEYWORDS)

#test if a keyword is in the list of keywords for a category

"vpn" in KEYWORDS["Network"]
"souris" in KEYWORDS["Hardware"]
"ventillateur" in KEYWORDS["Hardware"]

def classify(title, description):
    title_description = title.strip().lower() + " " + description.strip().lower()
    text_split = title_description.split()
    word_count = len(text_split)

    if word_count < 3:
        return "Need_review"

    found_categories = []
    for category, words in KEYWORDS.items():
        for word in words:
            if word in title_description:
                found_categories.append(category)
                break
    if len(found_categories) == 0:
        return "Need_review"
    elif len(found_categories) == 1:
        return found_categories[0]
    else:
        return "Need_review"
    
#print(classify("VPN", "impossible de me connecter au vpn depuis chez moi"))
#print(classify("Excel", "excel plante sur le réseau de l'entreprise"))
#print(classify("Aide", "ça marche pas"))

def evaluate(): 
    
    with open('tickets.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        count = 0
        nbreTickets = 0
        for row in reader:
            nbreTickets += 1
            predicted = classify(row['title'], row['description']) 
            if predicted == row['expected_category']:
                status = "OK"
                count += 1   

            else:
                status = "ERROR"
                
            print(row['Id'], predicted , row['expected_category'], status)
        
    print("Total tickets: ", nbreTickets)    
    print("Total correct predictions: ", count)                     

        
if __name__ == "__main__":
    evaluate()