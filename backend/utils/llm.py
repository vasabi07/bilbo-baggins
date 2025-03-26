import openai
from dotenv import load_dotenv
load_dotenv()

client = openai.OpenAI()
def llm(prompt: str):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message