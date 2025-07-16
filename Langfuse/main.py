
from dotenv import load_dotenv
# from openai import OpenAI
from langfuse.openai import OpenAI

load_dotenv()

client = OpenAI()



#Zero short promnet = A model give a direct question and task 
SYSTEM_PROMENT = """
      you are a an AI export in coding. You Only kniow the java  and nothing else.
      you help user in solving there JAVA doubts only and nothing else.
      If User tried to ask something else apart from JAVA you can roust of them

"""

response = client.chat.completions.create(
      model="gpt-4.1-mini",
      messages=[
            {"role":"system","content":SYSTEM_PROMENT},
            {"role":"user","content":"Hey, My name is Navneet"},     
            {"role":"assistant","content":"How can I assist you with your Python coding questions today?"},  
       {"role":"user","content":"Hey, How can i make a tea without milk "},   
       {"role":"user","content":"Hey, How to write a code in java add tow numbwer in java  "}, 
      ]
)
 

print(response.choices[0].message.content) 
  