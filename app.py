import os
from dotenv import load_dotenv

# 1. Load .env
load_dotenv()

# 2. Quick check to see if the key is coming through
print("Loaded key:", os.getenv("OPENAI_API_KEY"))  

from openai import OpenAI

# 3. Now instantiate the client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 4. Simple test call
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is 2 + 2?"}
    ]
)
print("Got reply:", response.choices[0].message.content)

