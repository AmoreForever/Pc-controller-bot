from lightdb import LightDB

db = LightDB("db/mdb.json")

def set_on_off(val: str) -> bool:
    db.set_key('starter', 'restart', val)
    
    
def get_on_off():
    return db.get_key('starter', "restart")


def set_message_id(val: int):
    db.set_key('starter', 'last_id', val)
    
    
def get_message_id():
    return db.get_key('starter', "last_id")


def get_status():
    return db.get_key('live', "status")

def set_status(val: str):
    db.set_key('live', 'status', val)