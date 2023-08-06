## ChatGPTBlock
A Python package for interacting with OpenAI's chat models through the OpenAI API.

### Installation
Before using the ChatGPTBlock class, make sure you have installed the necessary packages:

`pip install openai tiktoken requests`

### Install Locally
`pip install -e .`

### Install With PIP


## Usage

### Creating The Conversation
Here's an example of how to use the ChatGPTBlock class:
There are two options of using the class. Streamable and non-streamable.

```
from chat_gpt_block import ChatGPTBlock

# Initialize the ChatGPTBlock instance
chat_gpt_block = ChatGPTBlock(
    system_prompt="You are a helpful assistant.",
    openai_api_token="your_openai_api_key",
    model="gpt-4",
)

# Get a response from the model
response = chat_gpt_block("Tell me a joke.")
print(response)
```
    
```
from chat_gpt_block import ChatGPTBlock

chat_gpt_block = ChatGPTBlock(
    system_prompt="You are a helpful assistant.",
    openai_api_token="your_openai_api_key",
    model="gpt-4",
    stream=True
)

generator = chat_gpt_block("Tell me a joke.")
for token in generator:
    print(token, flush=True, end='')
```

### Resetting The Conversation

```
chat_gpt_block("Tell me a joke.")
print(chat_gpt_block.answer)

chat_gpt_block.reset()

response = chat_gpt_block("Tell me a story.")
print(response)
```

### Custom Preprocessor Function
```
from chat_gpt_block import ChatGPTBlock

def custom_preprocessor(input_text: str, some_dictionary: dict, prologue: str) -> str:
    return f"{prologue}\n{input_text}. {some_dictionary}"

chat_gpt_block = ChatGPTBlock(
    system_prompt="You are a helpful assistant.",
    openai_api_token="your_openai_api_key",
    model="gpt-4",
    preprocessor=custom_preprocessor,
)

response = chat_gpt_block(input_text="please check whether this python dictionary is valid", some_dictionary={"hello": "world"}, prologue='')
print(response)
```

### Custom Error Handling Function
```
from chat_gpt_block import ChatGPTBlock

def custom_error_handler():
    print("There was an error when communicating with OpenAI API. Please try again later")

chat_gpt_block = ChatGPTBlock(
    system_prompt="You are a helpful assistant.",
    openai_api_token="your_openai_api_key",
    model="gpt-4",
    on_error=custom_error_handler,
)

response = chat_gpt_block("tell me a joke")
print(response)
```

### Feeding The Model With The Examples
```
from chat_gpt_block import ChatGPTBlock

examples = [
    ("Please add a vegetable to an animal", "Alpaca + avocado = alpacavocado"),
    ("Now I want something with cats", "Cat + Cappuccino = cappucicatto"),
]

chat_gpt_block = ChatGPTBlock(
    system_prompt=
    """You are a helpful assistant with a sense of humor. 
       You know everything about animals, vegetables and how to combine them. 
       You must add animals to vegetables no matter what to create funny words.
    """,
    examples=examples,
    openai_api_token="your_openai_api_key",
    model="gpt-4",
)

response = chat_gpt_block("Make up some new word with \"tortoise\"")
print(response)
```


