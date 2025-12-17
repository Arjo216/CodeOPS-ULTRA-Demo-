import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load the API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found in .env file.")
    exit()

print(f"🔑 Using API Key: {api_key[:10]}********")

# 2. Configure the library
genai.configure(api_key=api_key)

# 3. List Models
print("\n📡 Fetching available models from Google AI Studio...")
try:
    models_found = False
    for m in genai.list_models():
        # Only show models that can generate content (text/code)
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Found: {m.name}")
            models_found = True
            
    if not models_found:
        print("⚠️ No models found with 'generateContent' capability.")
        print("This usually means the API key is invalid or has no service enabled.")

except Exception as e:
    print(f"❌ Error fetching models: {e}")
    print("\n💡 Troubleshooting Tips:")
    print("1. Check your internet connection (Firewalls often block gRPC).")
    print("2. Ensure your API Key is from 'Google AI Studio' (Free Tier).")