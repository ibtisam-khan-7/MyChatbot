import json
import google.generativeai as genai
from datetime import datetime
from difflib import get_close_matches

# --- CONFIGURATION ---
API_KEY = "AIzaSyCA6t5Zdsw5wG8XQp660R9zuygVeT8AU3M"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

class ChatBot:
    def __init__(self, name, personality="Professional", data_file="brain.json"):
        self.name = name
        self.is_active = True
        self.data = self.load_knowledge(data_file)
        self.pdf_context = ""
        
        # --- PERSONALITY MODES ---
        prompts = {
            "Professional": "You are Lily, a highly professional AI assistant. Keep answers concise, elegant, and polite.",
            "Friendly": "You are Lily, a cheerful and friendly AI companion. Use emojis, speak casually, and be helpful like a best friend.",
            "Funny": "You are Lily, a sarcastic and witty AI. Make jokes, be a bit savage but helpful.",
            "Code Guru": "You are Lily, a Python Expert. Explain everything with code examples and technical logic only."
        }
        
        selected_instruction = prompts.get(personality, prompts["Professional"])

        # --- UNIVERSAL FIX (No Config Error) ---
        initial_history = [
            {
                "role": "user",
                "parts": [f"System Instruction: {selected_instruction}"]
            },
            {
                "role": "model",
                "parts": ["Understood. I will adopt this persona."]
            }
        ]

        try:
            
            self.chat = model.start_chat(history=initial_history)
        except Exception as e:
            print(f"Error: {e}")
            self.chat = model.start_chat(history=[])

    def load_knowledge(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def ask_gemini(self, user_text):
        if not self.chat:
            return "Connection Error."

        try:
            if self.pdf_context:
                prompt = f"Context: {self.pdf_context}\n\nUser: {user_text}"
                response = self.chat.send_message(prompt)
            else:
                response = self.chat.send_message(user_text)
            
            return response.text
        except:
            return "Internet Connection Error."

    def process_input(self, user_text):
        user_text_lower = user_text.lower()
        
        # Simple Logic
        knowledge_keys = list(self.data.keys())
        matches = get_close_matches(user_text_lower, knowledge_keys, n=1, cutoff=0.8)

        if matches:
            return self.data[matches[0]]

        return self.ask_gemini(user_text)