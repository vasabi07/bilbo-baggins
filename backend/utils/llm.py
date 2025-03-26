import openai
from dotenv import load_dotenv
load_dotenv()

llm_client = openai.OpenAI()
def llm(prompt: str):
    response = llm_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        
    )
    return response.choices[0].message