import os, sys

from src.utils.database_handler import MongodbClient
from src.exeception import CustomException
from src.logger import logging

class MetaDataStore:

    def __init__(self):
        self.root = os.getcwd()
        self.images = os.path.join(self.root, "caltech-101")
        self.labels = os.listdir(self.images)
        self.mongo = MongodbClient()
    
    def register_labels(self):
        '''
        Adds images labels to our mongodb client
        '''
        try:
            records = {}
            for num, label in enumerate(self.labels):
                records[f"{num}"] = label

            self.mongo.database['labels'].insert_one(records)
            logging.info("Created")
            return {"Created", True}
        except Exception as e:
            error = CustomException(e, sys)
            logging.error("Could not create")
            return {"Created": False, "Reason": error.error_message}
    
    def run_step(self):
        '''
        runs the steps to complete the task for this class
        '''
        try:
            self.register_labels()
            logging.info("Created")
            return {"Created", True}
        except Exception as e:
            error = CustomException(e, sys)
            logging.error("Could not create")
            return {"Created": False, "Reason": error.error_message}


if __name__ == "__main__":
    meta = MetaDataStore()
    meta.run_step()

