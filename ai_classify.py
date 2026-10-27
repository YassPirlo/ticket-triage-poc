from google import genai
from dotenv import load_dotenv

import json

load_dotenv()

client = genai.Client()
prompt = """tu dois classer des tickets d'incidents informatiques dans les catégories suivantes : Network, Hardware, Software, Access, Email, Security, Need_review, utilise Need_review si tu n'es pas sûr de la catégorie, réponds uniquement en JSON qui contient category,confidence (high ou low) et reason (une phrase courte en anglais)"""

title="excel plante avec le VPN"
description="je n'arrive pas à ouvrir excel depuis que je suis connecté au VPN"

title_description = f"title: {title}\ndescription: {description}"
response = client.models.generate_content(model="gemini-3.6-flash",contents=title_description + "\n\n" + prompt, config={"response_mime_type":"application/json"})

print(response.text)
print("--------------------")
result = json.loads(response.text)
print(f"Category: {result['category']} | Confidence: {result['confidence']} | Reason: {result['reason']}")

