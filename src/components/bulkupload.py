import os
import base64
from from_root import from_root 
from tqdm import tqdm
from src.logger import logging
from src.exeception import CustomException

def upload_bulk_data(root_dir: str ="caltech-101"):
    '''
    Gets all the data from the root_dir directory
    '''
    labels = os.listdir(root_dir)

    for label in tqdm(labels):
        data = []
        images = os.listdir(root_dir + '/' + label)
        for img in tqdm(images):
            path = os.path.join(from_root(), root_dir, label, img)
            with open(rf"{path}", "rb") as img:
                data.append(base64.b64encode(img.read()).decode())

upload_bulk_data()






