import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY was not found in your .env file")
    exit()

print(f"API key found: {api_key[:3]}...{api_key[-4:]}")

try:
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Say exactly: Gemini API is working!"
    )

    print("\n✅ SUCCESS!")
    print("Gemini response:")
    print(response.text)

except Exception as e:
    print("\n❌ API CALL FAILED")
    print(type(e).__name__)
    print(e)