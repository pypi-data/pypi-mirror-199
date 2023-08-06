import asyncio

from ceylon import ceylon
from ceylon.agent import Message


class CeylonAI:

    def __init__(self):
        self._agents = {}

    def register(self, name):
        agent_data = {
            "name": name,
            "init": None,
            "processors": {},
            "backgrounds": {}
        }

        def decorator(cls):
            cls_ = cls()
            pubsub = ceylon.PubSub()
            cls_.pubsub = pubsub
            cls_.id = pubsub.get_node_id()

            def send(agent, topic, message):
                data = Message(cls_.id, message).encode()
                msg = ceylon.python_string_to_vec_u8(data)
                res = cls_.pubsub.publish(f"{agent}/{topic}", msg)
                print(f"send result: {res}")

            cls_.send = send
            agent_data["agent"] = cls_
            self._agents[name] = agent_data
            return cls

        def init(func):
            agent_data["init"] = func
            return func

        decorator.init = init

        def processor(name):
            def _decorator(func):
                agent_data["processors"][name] = func
                return func

            return _decorator

        decorator.processor = processor

        def background(name):
            def _decorator(func):
                agent_data["backgrounds"][name] = func
                return func

            return _decorator

        decorator.background = background

        return decorator

    async def __start__(self):
        agents_tsk = [asyncio.create_task(self.async_start_agent(agent_data)) for agent_data in self._agents.values()]
        await asyncio.gather(*agents_tsk)

    async def async_start_agent(self, agent_data):
        if agent_data["init"]:
            await agent_data["init"](agent_data["agent"])

        print(f"Agent {agent_data['agent'].id} started")
        print(f"Agent {agent_data['processors']}")

        async def __process_message__(data):
            # print(f"Agent {agent_data['agent'].id} received message")
            message = Message.decode(data)
            processors = [asyncio.create_task(processor(agent_data["agent"], message.message)) for processor in
                          agent_data['processors'].values()]
            await asyncio.gather(*processors)

        async def __subscribe__():
            print(f"Agent {agent_data['agent'].id} subscribed")
            print(f"Agent {agent_data['processors']}")
            await agent_data['agent'].pubsub.subscribe("agent_topic", __process_message__)

        async def start_subscriber():
            await agent_data["agent"].pubsub.start()

        bg_tsk = [asyncio.create_task(background(agent_data["agent"])) for background in
                  agent_data["backgrounds"].values()]

        tx1 = asyncio.create_task(__subscribe__())
        tx2 = asyncio.create_task(start_subscriber())
        await asyncio.gather(tx1, tx2, *bg_tsk)

    async def __finish__(self):
        print("finish")

    def start(self):
        try:
            # your code here
            asyncio.run(self.__start__())
        except KeyboardInterrupt:
            asyncio.run(self.__finish__())
        finally:
            print("finally")
