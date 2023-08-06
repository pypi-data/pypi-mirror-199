# DevGround

## ChatGPT API wrapper

This is a wrapper for the [ChatGPT API](https://platform.openai.com/docs/introduction) by [DevGround](https://devground.cz/).

### Model

gpt-3.5-turbo

### License

It is licensed under the MIT license.

### Language

Written in Python 3.11

### Requirements

requires environment variables:

- OPENAI_API_KEY

### Installation

install the package with pip:

```bash
pip install dg_chatgpt_api
```

### Usage

```python
from dg_chatgpt_api import ChatGPTAPI as api

api.reconnect()
api.add_user("user_id", "username")
api.add_conversation("user_id")
message = {
    "role": "user",
    "content": "message"
}
response = api.get_response("user_id", message)
```
