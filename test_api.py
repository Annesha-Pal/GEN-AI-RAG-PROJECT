import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

question = input("Ask a question: ")

response = client.interactions.create(
    model="gemini-3.6-flash",
    input=question
)

print("\nGemini's Answer:")
print(response.output_text)