import asyncio
import logging
import time

FORMAT = '%(levelname)s %(name)s %(asctime)-15s %(filename)s:%(lineno)d %(message)s'
logging.basicConfig(format=FORMAT)
logging.getLogger().setLevel(logging.INFO)

from .ceylon import *

__doc__ = ceylon.__doc__
if hasattr(ceylon, "__all__"):
    __all__ = ceylon.__all__

from .agent import Agent
from .agent_manager import AgentManager

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
