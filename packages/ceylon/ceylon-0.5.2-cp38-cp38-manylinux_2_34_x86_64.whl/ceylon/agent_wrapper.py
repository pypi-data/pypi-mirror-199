import asyncio
import pickle
import time
from typing import Dict

from ceylon import ceylon


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

    def __init__(self, name, _agent_class=None, _processors={}, _backgrounds={}):
        self._name = name
        self._init = None
        self._processors: Dict[str, Processor] = _processors
        self._backgrounds: Dict[str, Background] = _backgrounds
        self._agent_class = None
        self._agent = None

    def setup(self):
        cls_ = self._agent_class()
        pubsub = ceylon.PubSub()
        cls_.pubsub = pubsub
        cls_.id = pubsub.get_node_id()
        cls_.name = self._name

        def send(topic, message):
            data = Message(cls_.id, message).encode()
            msg = ceylon.python_string_to_vec_u8(data)
            res = cls_.pubsub.publish(f"{cls_.id}/{topic}", msg)
            return res

        cls_.send = send
        self._agent = cls_

    def set_init(self, func):
        self._init = func

    def set_agent(self, agent_cls):
        self._agent_class = agent_cls

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

    @property
    def agent(self):
        return self._agent

    async def init(self):
        if self._init is not None:
            await self._init(self._agent)

    async def process_message__(self, data):
        message: Message = Message.decode(data)
        if message is not None:
            processors = [asyncio.create_task(processor(self.agent, message.message)) for processor in
                          self.processors.values()]
            await asyncio.gather(*processors)

    async def subscribe(self):
        await self.agent.pubsub.subscribe("agent_topic", self.process_message__)

    async def start_agent(self):
        self.setup()
        await self.init()

        async def start_subscriber():
            await self.agent.pubsub.start()

        bg_tsk = [asyncio.create_task(background(self.agent)) for background in
                  self.backgrounds.values()]

        async def subscribe():
            await self.subscribe()

        tx1 = asyncio.create_task(subscribe())
        tx2 = asyncio.create_task(start_subscriber())
        await asyncio.gather(tx1, tx2, *bg_tsk)
