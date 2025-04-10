import redis
import json

class ConversationStore:
    def __init__(self,host="localhost",port=6379,db=0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
    def get_history(self,thread_id:str)-> dict:
        data = self.client.get(f"thread:{thread_id}")
        if data:
            return json.loads(data)
        else:
            return {"messages": []}
    def save_history(self,thread_id:str,state:dict)-> None:
        self.client.set(f"thread:{thread_id}",json.dumps(state))

conversation_store = ConversationStore()



        
