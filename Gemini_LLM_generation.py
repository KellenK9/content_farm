import google.generativeai as genai  # PAckage conflicts. Not currently in use
import os

genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content("Write a story about a AI and magic")
print(response.text)
