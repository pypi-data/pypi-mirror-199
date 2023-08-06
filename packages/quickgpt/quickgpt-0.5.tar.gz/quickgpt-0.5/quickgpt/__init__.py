from quickgpt.thread import Thread

__version__ = "0.5"

import os

class QuickGPT:
    def __init__(self, api_key=None):
        if not api_key:
            api_key = os.environ.get("OPENAI_API_KEY")

        self.api_key = api_key

        self.threads = []

    def new_thread(self):
        """ Creates a brand new Thread. """

        thread = Thread(self)

        self.threads.append(thread)

        return thread

    def restore_thread(self, obj):
        """ Restores an existing Thread, using the dict format
        returned by thread.serialize(). """

        thread = self.new_thread()
        thread.restore(obj)

        return thread

    def run(self, *messages):
        """ Quickly generate a one-off response without
        managing a full-blown Thread. """

        thread = self.new_thread()

        return thread.run(*messages)
