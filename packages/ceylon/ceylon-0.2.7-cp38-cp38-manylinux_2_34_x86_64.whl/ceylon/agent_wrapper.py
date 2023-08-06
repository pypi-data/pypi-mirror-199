import logging
import pickle
import time

from typing import Dict

class Processor:
    def __init__(self, agent, name, func):
        self.agent = agent
        self.name = name
        self.func = func

    async def __call__(self, message):
        return await self.func(self.agent, message)


class Background:
    def __init__(self, agent, name, func):
        self.agent = agent
        self.name = name
        self.func = func

    async def __call__(self, *args, **kwargs):
        return await self.func(self.agent, *args, **kwargs)


class Message:
    def __init__(self, agent_id, message):
        self.id = agent_id + "/" + str(time.time())
        self.message = message

    @staticmethod
    def decode(data):
        try:
            data = pickle.loads(data)
            if "id" in data and "message" in data:
                return Message(data["id"], data["message"])
        except Exception as e:
            return None

    def encode(self):
        return pickle.dumps({"id": self.id, "message": self.message})


class AgentWrapper:

    def __init__(self, name):
        self._name = name
        self.init = None
        self._processors: Dict[str, Processor] = {}
        self._backgrounds: Dict[str, Background] = {}
        self.agent = None

    def add_processor(self, name, func: Processor):
        self._processors[name] = func

    def add_background(self, name, func: Background):
        self._backgrounds[name] = func

    @property
    def name(self):
        return self._name

    @property
    def processors(self) -> Dict[str, Processor]:
        return self._processors

    @property
    def backgrounds(self) -> Dict[str, Background]:
        return self._backgrounds
