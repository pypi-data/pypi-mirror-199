import json
from llama_cpp import Llama

llm = Llama(model_path="models/ggml-alpaca-7b-q4.bin")

output = llm("Q: Name the planets in the solar system? A: ", max_tokens=32, stop=["Q:", "\n"], echo=True)

print(json.dumps(output, indent=2))