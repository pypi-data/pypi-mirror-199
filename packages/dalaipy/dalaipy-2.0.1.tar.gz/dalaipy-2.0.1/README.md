# dalaipy
A Python Wrapper for [Dalai](https://github.com/cocktailpeanut/dalai)!

Dalai is a simple, and easy way to run LLaMa and Alpaca locally.

## Installation
`pip install dalaipy`

## Instructions
1. Go to [Dalai](https://github.com/cocktailpeanut/dalai), and set up your model of choice on your system (either Mac, Windows, or Linux). The readme provides clear explanations!
2. Once you can run `npx dalai serve`, run the server and test out your model of choice.
3. Install dalaipy per the instructions above, and make your first request:
```
from dalaipy.src import Dalai

model = Dalai()
# your_model can be one of the following, "alpaca.7B", "alpaca.13B", "llama.7B", "llama.13B", "llama.30B", or "llama.65B", and is dictated by which model you installed
request = model.generate_request("What is the capital of the United States?", your_model)
print(model.generate(request))
```