import google.generativeai as genai

API_KEY = "YAHAN_APNI_KEY_PASTE_KAREIN"
genai.configure(api_key=API_KEY)

print("Checking available models...")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)