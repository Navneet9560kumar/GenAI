import tiktoken


enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hello, world! i am Navneet"
tokens = enc.encode(text)
tokens = [13225, 11, 2375, 0, 575, 939, 17271, 141755]
decode = enc.decode(tokens)
print("Tokens:", tokens)
print("Decoded text:", decode)
