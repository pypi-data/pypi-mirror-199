import openai

from uuid import uuid4

from quickgpt.thread.messagetypes import *
from quickgpt.thread.response import Response

class Thread:
    def __init__(self, quickgpt):
        self.quickgpt = quickgpt

        openai.api_key = quickgpt.api_key

        self.thread = []
        self.id = str(uuid4())

    def __len__(self):
        """ Returns the length of the thread """
        return len(self.thread)

    def serialize(self):
        """ Returns a serializable, JSON-friendly dict with all of the
        thread's data. Can be restored to a new Thread object later. """

        return {
            "__quickgpt-thread__": {
                "id": self.id,
                "thread": self.messages
            }
        }

    def restore(self, obj):
        """ Restores a serialized Thread object,
        provided by thread.serialize() """

        thread_dict = obj["__quickgpt-thread__"]
        self.id = thread_dict["id"]

        self.feed(thread_dict["thread"])

    def clear(self, include_sticky=False):
        """ Resets the thread, preserving only messages that were
        marked as sticky - unless include_sticky is set to True."""

        for message in self.thread:
            if not message.sticky or include_sticky:
                self.thread.remove(message)

    def feed(self, *messages):
        """ Appends a new message to the thread feed. """

        try:
            # Check if the first argument is a list, and then make it the parent
            iter(messages[0])
            messages = messages[0]
        except TypeError:
            pass

        for msg in messages:
            assert type(msg) in (System, Assistant, User, Response, dict), \
                "Must be of type System, Assistant, User, Response, or dict"

            if type(msg) == Response:
                msg = Assistant(msg.message)

            # Convert a boring old dict message to a pretty object message
            if type(msg) == dict:
                role = msg["role"]
                content = msg["content"]

                if role == "system":
                    msg = System(content)
                elif role == "assistant":
                    msg = Assistant(content)
                elif role == "user":
                    msg = User(content)
                else:
                    raise TypeError("Unknown role '%s'" % role)

            self.thread.append(msg)

    @property
    def messages(self):
        """ Returns a JSON-safe list of all messages in this thread """
        return [ msg.obj for msg in self.thread ]

    def run(self, feed=True):
        """ Executes the current thread and get a response. If `feed` is
        True, it will automatically save the response to the thread. """
        messages = self.messages

        response_obj = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        response = Response(response_obj)

        if feed:
            self.feed(response)

        return response

    def moderate(self, prompt):
        """ Validate a prompt to ensure it's safe for OpenAI's policies """
        
        response = openai.Moderation.create(
            input=prompt
        )

        output = response["results"][0]

        return output
