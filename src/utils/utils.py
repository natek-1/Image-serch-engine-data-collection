import uuid

def unique_image_name() -> str:
    return "img-" + str(uuid.uuid1())
