from google import genai
import os

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
prompt = "Write a story about"
output = client.models.generate_content(model="gemini-flash-latest", contents=prompt)
print(output.text.strip())
