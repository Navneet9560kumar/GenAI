from dotenv import load_dotenv
from openai import OpenAI
import json
load_dotenv()

client = OpenAI()

#Chai of thought: The modle is encouraged to breack down resoing step before arriving at 
SYSTEM_PROMENT = """
      You are a helpful AI assistant who is specialized in resolving user query.
      For the given user input , analyse the input and brack down step by step

      The stpe a user input, you analyse, you think , you think agian, and think for servera 

      Follow he stpe n sequence that is "anaylse","think","output","validate" and finally ""result"

      Rules:
      1. Follow the strict JOSN output as per schema.
      2. Always peerform one step at a time wait a next input
      3.Carefully anaylse the user query,


      Output Format:
      {{"step":"string", "content":""String"}}


      Example:
      Input:What is 2+2 
      output:{{"step":"anylyse","content":"Alight! The user is interst in math query and he is asking a base a arthmatic question "}}

      
       output:{{"step":"think","content":"To perform this addition ,I must go from left to right and add all operations "}}

        output:{{"step":"output","content":"4 "}}
         output:{{"step":"validate","content":"Seems Like 4 is coorect ans for 2+ 2 "}}
          output:{{"step":"result","content":"2+ 2= 4 and this is calcutate byy adding all number"}}

          
      Example:
Input: What is 2 + 2 * 5 / 3

output: {"step": "analyse", "content": "Alright! The user is asking a mathematical question involving basic arithmetic operations."}

output: {"step": "think", "content": "To solve this expression, I need to follow the BODMAS rule (Brackets, Orders, Division/Multiplication, Addition/Subtraction)."}

output: {"step": "validate", "content": "Correct, applying BODMAS is the right approach here."}

output: {"step": "think", "content": "First, I need to solve the division: 5 / 3 = 1.66666666."}

output: {"step": "validate", "content": "Correct, as per BODMAS, division comes before multiplication and addition."}

output: {"step": "think", "content": "Now that 5 / 3 = 1.666..., the expression becomes: 2 + 2 * 1.66666666."}

output: {"step": "validate", "content": "Yes, the updated expression is correct as per the rule."}

output: {"step": "think", "content": "Next, perform the multiplication: 2 * 1.66666666 = 3.33333332. Now the expression becomes: 2 + 3.33333332."}

output: {"step": "output", "content": "The final result after performing the addition: 2 + 3.33333332 = 5.33333332."}

output: {"step": "validate", "content": "Yes, all calculations are correct based on the BODMAS rule."}

output: {"step": "result", "content": "Using BODMAS, the expression 2 + 2 * 5 / 3 evaluates to approximately 5.33333332."}

"""

# response = client.chat.completions.create(
#     model="gpt-4.1-mini",  # Use "gpt-4o" instead of gpt-4.1-mini
#   response_format={"type": "json_object"},
#     messages=[
#         {"role": "system", "content": SYSTEM_PROMENT},
#         {"role": "user", "content": "What is 5 / 2 * 3 to the power 4? Please respond in JSON."},
#         {"role": "assistant", "content": json.dumps({"step":"analyse", "content":"The user is asking to evaluate the mathematical expression 5 / 2 * 3 to the power 4."})},

#          {"role": "assistant", "content": json.dumps({"step": "think", "content": "First, calculate 3 to the power 4, which is 3^4 = 81. Then, divide 5 by 2, which is 2.5. Finally, multiply 2.5 by 81 to get the result."})},

#          {"role": "assistant", "content": json.dumps({"step": "output", "content": "3^4 = 81; 5 / 2 = 2.5; 2.5 * 81 = 202.5. Hence, the result is 202.5."})},
#          {"role": "assistant", "content": json.dumps({"step": "validate", "content": "Rechecking calculations: 3^4 = 81 is correct. 5 / 2 = 2.5 is correct. 2.5 * 81 = 202.5 is correct. All steps are accurately calculated."})},

#            {"role": "assistant", "content": json.dumps({"step": "result", "content": "The value of the expression 5 / 2 * 3^4 is 202.5."} )},
#     ]
# )

# print("\n\n🤖🤖🤖", response.choices[0].message.content, "\n\n")


messages = [
    {"role": "system", "content": SYSTEM_PROMENT}
]

query = input(">") + " Please respond in JSON format."  # ✅ Append this
messages.append({"role": "user", "content": query})

while True:
   response=client.chat.completions.create(
            model="gpt-4o",  # ✅ FIXED only this line
            response_format={"type": "json_object"},
            messages=messages
      )
   messages.append({"role" : "assistant","content":response.choices[0].message.content})
   parsed_response = json.loads(response.choices[0].message.content)

   if parsed_response.get("step")!= "result":
      print("        🧠:", parsed_response.get("content"))
      continue

   print("🤖" , parsed_response.get("content"))
   break
