import json
import logging
import os
import openai
import dg_chatgpt.config as config
from dg_chatgpt.models import User, Conversation

config.setup()


users = {}
conversations = {}


def reconnect():
    config.setup()


def add_user(id, name):
    """Add a user to the list."""
    if id not in users:
        users[id] = User(id, name)


def get_user(id):
    """Get a user from the list."""
    if id not in users:
        return None
    return users[id]


def add_conversation(user_id):
    """Add a conversation to the list."""
    if user_id not in users:
        return None
    if user_id not in conversations:
        conversations[user_id] = Conversation(
            user_id, config.INTRO_PROMPT)


def get_conversation(user_id):
    """Get a conversation from the list."""
    if user_id not in conversations:
        return None
    return conversations[user_id]


def get_response(user_id, message):
    """Get a response from the chatbot."""
    conversation = get_conversation(user_id)
    if conversation is None:
        return None
    response = conversation.get_response(message)
    return response


def log_conversation(user_id):
    """Log a conversation to a file."""
    conversation = get_conversation(user_id)
    if conversation is None:
        return
    conversation.log()


if __name__ == "__main__":
    print("This is a module, not a script.")
    exit()
