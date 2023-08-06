import asyncio
import copy
import logging
import multiprocessing
import os

import ceylon.ceylon
from art import text2art

from .agent_wrapper import Message

my_art = text2art("Ceylon-AI", font='tarty1')  # Notice the space between "SPACE" and "ART"
print(my_art)
my_art = text2art("ceylon.ai", font='fancy144')  # Notice the space between "SPACE" and "ART"
print(my_art)
my_art = text2art("version 0.2.5", font='fancy144')  # Notice the space between "SPACE" and "ART"
print(my_art)

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger("RAKUN-MAS")

from .ceylon import *

__doc__ = ceylon.__doc__
if hasattr(ceylon, "__all__"):
    __all__ = ceylon.__all__

from .agentdecorator import AgentDecorator


# from .agent_manager import CeylonAI

class AgentWrapper:
    def __init__(self, agent_class, name, background_processors, message_processors):
        pubsub = ceylon.ceylon.PubSub()
        self.agent = agent_class()
        self.agent.name = name
        self.agent.id = pubsub.get_node_id()
        self.pubsub = pubsub
        self.background_processors = background_processors
        self.message_processors = message_processors
        self.agent.wrapper = self
        # self.agent.send = self.send

    def send(self, topic, message):
        data = Message(self.agent.id, message).encode()
        msg = ceylon.python_string_to_vec_u8(data)
        res = self.pubsub.publish(f"{self.agent.id}/{topic}", msg)

    async def __subscribe_to_pubsub__(self):
        async def process_message(data):
            message: Message = Message.decode(data)
            if message is not None:
                processors = [asyncio.create_task(processor(self.agent, message.message)) for processor in
                              self.message_processors.values()]
                await asyncio.gather(*processors)

        self.pubsub.subscribe("agent_topic", process_message)
        await self.pubsub.start()

    async def run(self):
        if hasattr(self.agent, "setup_method") and self.agent.setup_method is not None:
            await self.agent.setup_method()

        sub_tx = asyncio.create_task(self.__subscribe_to_pubsub__())

        background_tasks = []
        for name, processor in self.background_processors.items():
            background_tasks.append(asyncio.create_task(processor(self.agent)))

        await asyncio.gather(sub_tx, *background_tasks)


class CeylonAIAgent:

    def __init__(self):
        self.__agent__cls = None
        self.__agent_initial_method = None
        self.__message_processors = {}
        self.__background_processors = {}
        self.__number_of_agents = 1
        self.__agent__name = None

    def register(self, name, number_of_agents=1):
        def decorator(cls):
            self.__number_of_agents = number_of_agents
            self.__agent__name = name
            self.__agent__cls = cls
            self.__agent__cls.setup_method = self.__agent_initial_method
            return cls

        return decorator

    def init(self):
        def decorator(func):
            self.__agent_initial_method = func
            return func

        return decorator

    def background(self, name=None):
        def decorator(func):
            _name = name or func.__name__
            self.__background_processors[_name] = func
            return func

        return decorator

    def processor(self, name=None):
        def decorator(func):
            _name = name or func.__name__
            self.__message_processors[_name] = func
            return func

        return decorator

    def __start__(self):
        agent_tx = []
        for i in range(self.__number_of_agents):
            agent_class = copy.deepcopy(self.__agent__cls)
            message_processors = copy.deepcopy(self.__message_processors)
            background_processors = copy.deepcopy(self.__background_processors)
            agent_name = copy.deepcopy(self.__agent__name)
            agent_name = f"{agent_name}-{i}"
            agent = AgentWrapper(agent_class, agent_name, background_processors,
                                 message_processors)
            print(f"Starting {agent.agent.name} {agent.agent.id}")

            # agent_tx.append(asyncio.create_task(agent.run()))
            def run(agent):
                try:
                    asyncio.run(agent.run())
                except KeyboardInterrupt:
                    print(f"Bye Bye {agent.agent.name} {agent.agent.id}")
                    exit(0)

            tx = multiprocessing.Process(target=run, args=(agent,))
            agent_tx.append(tx)

        try:
            # await asyncio.gather(*agent_tx)
            for task in agent_tx:
                task.start()

            for task in agent_tx:
                task.join()
        except KeyboardInterrupt:
            print("Bye Bye")
            exit(0)

    def run(self):
        self.__start__()


class CeylonAI:

    def __init__(self):
        self.__agents = []

    def agent(self):
        agent = CeylonAIAgent()
        self.__agents.append(agent)
        return agent

    def run(self):
        try:
            agent_tx = []
            for agent in self.__agents:
                tx = multiprocessing.Process(target=agent.run)
                agent_tx.append(tx)

            for task in agent_tx:
                task.start()

            for task in agent_tx:
                task.join()
        except KeyboardInterrupt:
            print("Bye Bye")
            exit(0)
