import openai
import os
import logging
import json
from dotenv import load_dotenv


OPENAI_API_KEY = ""
INTRO_PROMPT = {}


def setup():
    """Setup the OpenAI API key from the environment variable OPENAI_API_KEY."""

    load_dotenv()

    if not 'OPENAI_API_KEY' in os.environ:
        warning = 'No OpenAI API key found. Set the `OPENAI_API_KEY` environment variable.'
        logging.warning(warning)
        raise ValueError(warning)

    global OPENAI_API_KEY
    OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

    openai.api_key = OPENAI_API_KEY

    if not openai.api_key:
        warning = 'OpenAI API key is invalid'
        logging.warning(warning)
        print(warning)
        raise ValueError(warning)

    if not os.path.isfile("dg_chatgpt_config.json"):
        warning = 'No dg_chatgpt_config.json file found. Creating default one...'
        logging.warning(warning)
        print(warning)
        with open("dg_chatgpt_config.json", "w", encoding="utf-8") as f:
            f.write("""{
                "intro_prompt": {
                    "role": "system",
                    "content": "You are chatGPT assistant. Answer questions as concisely as possible."
                }
            }""")

    with open("dg_chatgpt_config.json", "r") as f:
        config = json.load(f)
        if not "intro_prompt" in config:
            warning = 'No `intro_prompt` found in config.json. Please add one.'
            logging.warning(warning)
            print(warning)
            raise ValueError(warning)

        if not "role" in config["intro_prompt"]:
            warning = 'No `role` found in `intro_prompt` in dg_chatgpt_config.json. Please add one.'
            logging.warning(warning)
            print(warning)
            raise ValueError(warning)

        if not "content" in config["intro_prompt"]:
            warning = 'No `content` found in `intro_prompt` in dg_chatgpt_config.json. Please add one.'
            logging.warning(warning)
            print(warning)
            raise ValueError(warning)

        global INTRO_PROMPT
        INTRO_PROMPT = config["intro_prompt"]

    if not os.path.exists("chat_logs"):
        info = 'No `chat_logs` directory found. Creating one...'
        logging.log(logging.INFO, info)
        print(info)

        os.mkdir("chat_logs")

    logging.log(logging.INFO, "OpenAI API key loaded successfully")
    print("OpenAI API key loaded successfully")


if __name__ == '__main__':
    print("This is a setup script. Please run `python3 -m chatgpt` instead.")
