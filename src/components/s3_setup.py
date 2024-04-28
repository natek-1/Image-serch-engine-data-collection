import os, sys, shutil


from dotenv import load_dotenv


from src.exeception import CustomException
from src.logger import logging

load_dotenv()
class DataStore:
    def __init__(self):
        self.root = os.getcwd()
        self.zip = os.path.join(self.root, "archive.zip")
        self.images = os.path.join(self.root, "caltech-101")
        self.list_unwanted = ["BACKGROUND_Google"]


    def remove_unwanted_classes(self):
        '''
        the structure of the downloaded data is caltech-101/{label}
        some labels are not needed for example "BACKGROUND_Google" for our task so this function removes that
        '''
        try:
            logging.info("Removing classes that will not be needed for this project")
            for label in self.list_unwanted:
                path = os.path.join(self.images, label)
                shutil.rmtree(path, ignore_errors=True)
            logging.info("Removed uneeded classes for this project")

        except Exception as e:
            error = CustomException(e, sys)
            logging.error("Failed to remove all unwated classes" + error.error_message)
        

    def sync_data(self):
        '''
        The goal here is to sync the data in the data folder to what should be in our s3 bucket
        '''
        try:
            logging.info("--------Starting the sync with aws--------")
            os.system(f"aws s3 sync { self.images } { os.environ['AWS_S3_URI'] } ")
            logging.info("--------Completed sync of data with aws--------")
        except Exception as e:
            error = CustomException(e, sys)
            logging.error("Failed to Sync" + error.error_message)
    

    def run_step(self):
        '''
        runs the steps to complete the task for this class
        '''
        try:
            self.remove_unwanted_classes()
            self.sync_data()
            logging.info("Created")
            return {"Created", True}
        except Exception as e:
            error = CustomException(e, sys)
            logging.error("Could not create")
            return {"Created": False, "Reason": error.error_message}

if __name__ == "__main__":
    store = DataStore()
    store.run_step()
