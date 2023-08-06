import asyncio
import pickle
import time

import ceylon


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
        data = pickle.loads(data)
        return Message(data["id"], data["message"])

    def encode(self):
        return pickle.dumps({"id": self.id, "message": self.message})


class Agent:
    def __init__(self):
        self.pubsub = ceylon.PubSub()
        self.id = self.pubsub.get_node_id()
        self._agent = None
        self._processors = {}
        self._background = {}
        self._init = None
        print(f"Agent {self.id} created")

    def init(self):
        def decorator(func):
            self._init = func
            return func

        return decorator

    def register(self, name):
        def decorator(cls):
            self._agent = cls()
            self.name = name
            return self._agent

        return decorator

    def processor(self, name):
        def decorator(func):
            self._processors[name] = Processor(self._agent, name, func)
            return func

        return decorator

    def background(self, name):
        def decorator(func):
            self._background[name] = Background(self._agent, name, func)
            return func

        return decorator

    async def __process_message__(self, data):
        message = Message.decode(data)
        processors = [asyncio.create_task(processor(message.message)) for processor in
                      self._processors.values()]
        await asyncio.gather(*processors)

    async def __subscribe__(self):
        self.pubsub.subscribe("agent_topic", self.__process_message__)

    async def send(self, agent, topic, message):
        data = Message(self.id, message).encode()
        msg = ceylon.python_string_to_vec_u8(data)
        self.pubsub.publish(f"{agent}/{topic}", msg)

    async def __start__(self):
        if self._init:
            await self._init(self._agent)

        async def start_subscriber():
            await self.pubsub.start()

        tx1 = asyncio.create_task(self.__subscribe__())
        tx2 = asyncio.create_task(start_subscriber())
        tx_bg = [asyncio.create_task(bg()) for bg in self._background.values()]
        print(f"Starting agent {self.id} with {len(tx_bg)} background tasks")
        await asyncio.gather(tx1, tx2, *tx_bg)

    def start(self):
        asyncio.run(self.__start__())

    async def async_start(self):
        await self.__start__()
