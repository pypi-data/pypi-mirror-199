import asyncio
import logging
import pickle
import time

FORMAT = '%(levelname)s %(name)s %(asctime)-15s %(filename)s:%(lineno)d %(message)s'
logging.basicConfig(format=FORMAT)
logging.getLogger().setLevel(logging.INFO)

from .ceylon import *

__doc__ = ceylon.__doc__
if hasattr(ceylon, "__all__"):
    __all__ = ceylon.__all__


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

    def init(self):
        def decorator(func):
            self._init = func
            return func

        return decorator

    def register(self, name):
        def decorator(cls):
            self._agent = cls()
            self._agent.name = name
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


async def _start():
    async def python_callback(message):
        logging.info(f"---------------------------------------Python callback received: {message}")

    logging.info("-----------------------------------------Starting Python client")
    pubsub = ceylon.PubSub()
    id = pubsub.get_node_id()
    logging.info(f"---------------------------------------Python client id: {id}")
    await pubsub.subscribe("agent_topic", python_callback)

    async def pass_message():
        # await asyncio.sleep(10)
        # pubsub.publish("agent_topic", rk_python.python_string_to_vec_u8(f"Hello from Python! {id}"))
        while True:
            await asyncio.sleep(5)
            current_time_ns = time.time_ns()
            pubsub.publish("agent_topic",
                           ceylon.python_string_to_vec_u8(f"Hello from Python! {id} {current_time_ns}"))

    async def start_subscriber():
        await pubsub.start()

    tx = asyncio.create_task(pass_message())
    tx1 = asyncio.create_task(start_subscriber())

    await asyncio.gather(tx, tx1)


def start():
    asyncio.run(_start())
