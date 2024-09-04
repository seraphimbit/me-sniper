from automate import Automate # type: ignore
from dotenv import load_dotenv, find_dotenv # type: ignore
import os
import asyncio

load_dotenv(find_dotenv())

USER_KEY = os.getenv('USER_KEY')
RPC = os.getenv('RPC')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

automate = Automate()

automate._state['USER_KEY'] = USER_KEY
automate._state['RPC'] = RPC
automate._state['COLLECTION_NAME'] = COLLECTION_NAME

if __name__ == "__main__":
    asyncio.run(automate.Snipe())