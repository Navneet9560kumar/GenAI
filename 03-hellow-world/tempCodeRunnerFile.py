response = client.chat.completions.create(
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

