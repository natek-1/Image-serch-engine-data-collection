from typing import List, Union, Any

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from src.utils.database_handler import MongodbClient
from src.utils.s3handler import S3Connection

app = FastAPI(title="DataCollectorServer")
mongo = MongodbClient()
s3 = S3Connection()

choices = {}

@app.get("/fetch")
def fetch_label():
    global choices
    result = mongo.database['labels'].find()
    documents = [document for document in result]
    choices = dict(documents[0])
    response = {"Status": "Success", "Response": str(documents[0])}
    return JSONResponse(content=response, status_code=200, media_type="application/json")


@app.post("/add_label/{label_name}")
def add_label(label_name: str):
    result = mongo.database['labels'].find()
    documents = [document for document in result]
    last_value = list(map(int, list(documents[0].keys())[1:]))[-1]
    response = mongo.database['labels'].update_one({"_id": documents[0]["_id"]},
                                                   {"$set": {str(last_value + 1): label_name}})
    
    if response.modified_count == 1:
        response = s3.add_label(label_name)
        return {"Status": "Sucesses", "S3-response": response}
    else:
        return {"Status": "Fail", "Message": response[1]}

@app.get("/single_upload/")
def single_upload():
    '''
    get page to upload only one image
    '''
    info = {"Response": "Available",
            "Post-Request-Boby": ["label", "Files"]}
    return JSONResponse(content=info, status_code=200, media_type="application/json")


@app.post("/single_upload/")
async def single_upload(label: str, file: UploadFile = None):
    '''
    post method to upload a single image of a specified label
    input label: class of the label of the image
    input file: the file being uploaded
    '''
    label = choices.get(label, False) #check if label is in our list of choice{labels for dataset}
    if file.content_type == "image_jpeg" and label:
        response = s3.upload_to_s3(file.file, label)
        return {"filename": file.filename,
                "label": label,
                "S3-Response": response}
    else:
        return {
            "ContentType": f"Content type should be Image/jpeg not {file.content_type}",
            "label": label
        }
    
@app.get("/bulk_upload")
def bulk_upload():
    '''
    get page to upload multiples images of the same label
    '''
    info = {"Response": "Available",
            "Post-Request-Boby": ["label", "Files"]}
    return JSONResponse(content=info, status_code=200, media_type="application/json")

@app.post("/bulk_upload")
def bulk_upload(label: str, files: List[UploadFile] = File(...)):
    try:
        skippped = []
        final_response = None
        label: Union[str, Any] = choices.get(label, False)
        if label:
            for file in files:
                if file.content_type == "image_jpeg":
                    response = s3.upload_to_s3(file.file, label)
                    final_response = response
                else:
                    skippped.append(file.filename)
            return {
                "label": label,
                "skipped": skippped,
                "S3-respose": final_response,
                "LabelFound": label
            } 
        else:
            return {
                "label": label,
                "skipped": [file.filename for file in files],
                "S3-respose": final_response,
                "LabelFound": label
            }


    except Exception as e:
        return {"ContentType": f"got the following error {e}"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
