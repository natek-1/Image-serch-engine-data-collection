import os, sys
from typing import Dict

import boto3
from dotenv import load_dotenv

from src.utils.utils import unique_image_name
from src.exeception import CustomException
from src.logger import logging


load_dotenv()
class S3Connection:
    '''
    Class used to make and manage connection with S3 bucket
    '''
    def __init__(self):
        self.session = boto3.Session(
            aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        )
        self.s3 = self.session.resource("s3")
        self.bucket = self.s3.Bucket(os.environ['AWS_BUCKET_NAME'])
    

    def add_label(self, label: str) -> Dict:
        """
         This Function is responsible for adding label in s3 bucket.
         param label: the name of label 
         return: json Response of state message (success or failure)
         """
        try:
            key = f"images/{label}"
            response = self.bucket.put_object(Body="", Key=key)
            return {
                "Created": True, 
                "Path": response.key
            }
        except Exception as e:
            exception = CustomException(e, sys)
            return {
                "Created": False,
                "Reason": exception.error_message
            }
    
    def upload_to_s3(self, image_path: str, label: str):
        """
        This Function is responsible for uploading images in the predefined
        location in the s3 bucket.
        param: label: the name of the label
        param: image_path: the file path to the image to upload
        return: json Response of state message (success or failure)
        """
        try:
            self.bucket.upload_fileobj(
                image_path,
                f"images/{label}/{unique_image_name}.jpeg",
                ExtraArgs={"ACL": "public-read"}
            )
            return {"Created": True}
        except Exception as e:
            error = CustomException(e, sys)
            return {"Created": False, "Reason": error.error_message}


