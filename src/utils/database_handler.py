import pymongo
import os
from src.logger import logging
from src.exeception import CustomException
from dotenv import load_dotenv

load_dotenv()

class MongodbClient:

    def __init__(self, database_name: str = os.environ["DATABASE_NAME"]):
        uri = f"mongodb+srv://{os.environ['ATLAS_CLUSTER_USERNAME']}:{os.environ['ATLAS_CLUSTER_PASSWORD']}@learn.fz36e1j.mongodb.net/?retryWrites=true&w=majority&appName=Learn"
        self.client = pymongo.MongoClient(uri)
        self.database = self.client[database_name]
        self.database_name = database_name
