
import os
from dotenv import load_dotenv
from google import genai
 
# Load the .env file so we can read GEMINI_API_KEY
load_dotenv()
 
api_key = os.getenv("GEMINI_API_KEY")
 
if not api_key:
    print("❌ No API key found. Check your .env file has GEMINI_API_KEY=your-key")
else:
    client = genai.Client(api_key=api_key)
 
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input="Say hello and confirm you're working, in one short sentence."
    )
 
    print("✅ Connected successfully! Gemini says:")
    print(interaction.output_text)
