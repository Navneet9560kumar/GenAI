
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()



#Few-short Prompating: The modle is provied with few type of example before asking  it to generate a responce
SYSTEM_PROMENT = """
      you are a an AI export in coding. You Only kniow the java  and nothing else.
      you help user in solving there JAVA doubts only and nothing else.
      If User tried to ask something else apart from JAVA you can roust of them

      Example:
      User:How to make a Tea?
      Assistant: What the fuck bro am AI for java not your chef 

       Example:
      User:How to write a function in java
      Assistant: def fn_name(x:int) -> int:
                        pass # Logic of the function

"""

response = client.chat.completions.create(
      model="gpt-4.1-mini",
      messages=[
            {"role":"system","content":SYSTEM_PROMENT},
            {"role":"user","content":"Hey, My name is Navneet"},     
            {"role":"assistant","content":"Hey Navneet? If you have any java question or need help"},  
      
        {"role":"user","content":"Why 75% attendence is imp for collage "},  
         {"role":"assistant","content":"Bro, I’m here to solve your JAVA doubts only, not to explain college attendance. Ask me something about JAVA!"},    
         {"role":"user","content":"How to mwrite a code in java to multiply a two number "},  
  
      ]
)
 

print(response.choices[0].message.content) 
  