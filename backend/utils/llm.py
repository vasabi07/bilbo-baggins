import openai
from dotenv import load_dotenv
load_dotenv()
from utils.types import MessagesState

llm_client = openai.OpenAI()
def llm(messages: MessagesState):
    response = llm_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    return response.choices[0].message

if __name__=="__main__":
    print(llm("hey, how are you?"))