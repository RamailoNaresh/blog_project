import uuid

def get_char_uuid(length = None):
    uid = uuid.uuid4().hex
    if length:
        return uid[:length]
    return uid