import json
import logging
import os
import openai


class User:
    """A user in the chat."""

    def __init__(self, id, name):
        """Initialize a user."""
        self.id = id
        self.name = name

    def __repr__(self):
        """Return a string representation of the user."""
        return f'User({self.id}, {self.name})'

    def __str__(self):
        """Return a string representation of the user."""
        return f'User({self.id}, {self.name})'


class Conversation:
    """A conversation with the chatbot."""

    def __init__(self, user_id, intro_prompt):
        """Initialize a conversation."""
        self.user_id = user_id
        self.intro_prompt = intro_prompt
        self.messages = []

    def __repr__(self):
        """Return a string representation of the conversation."""
        return f'Conversation({self.user_id}, {self.messages})'

    def __str__(self):
        """Return a string representation of the conversation."""
        return f'Conversation({self.user_id}, {self.messages})'

    def get_response(self, message):
        """Get a response from the chatbot.
           Message should be a dictionary with a `role` and `content`. Role can be `user` or `system`."""

        if not "role" in message:
            warning = 'No `role` found in message. Please add one.'
            logging.warning(warning)
            return None

        if message["role"] != "user" and message["role"] != "system":
            warning = 'Role must be `user` or `system`.'
            logging.warning(warning)
            return None

        if not "content" in message:
            warning = 'No `content` found in message. Please add one.'
            logging.warning(warning)
            return None

        self.messages.append(message)
        prompt = self.messages.copy()
        prompt.insert(0, self.intro_prompt)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            user=self.user_id
        )
        self.messages.append(response.choices[0].message)

        if response.usage["total_tokens"] > 2048:
            info = f'OpenAI API usage nearing limit (tokens: {response.usage["total_tokens"]}). Clearing oldest message.'
            logging.log(logging.INFO, info)
            self.messages.pop(0)

        return response

    def clear(self):
        """Clear the conversation."""
        self.messages = []

    def log(self):
        """Log the conversation to a file."""
        path = os.path.join("chat_logs", f"{self.user_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=4)
