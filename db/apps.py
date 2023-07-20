from lightdb import LightDB

db = LightDB("db/apps.json")


def add_app(path, name):
    if name in list(db):
        return "The app already exists"
    ex = {f"{name}": {"path": f"{path}", "name": f"{name}"}}
    db.update(ex)
    db.save()


def del_app(name):
    del db[name]
    db.save()


def get_apps():
    return list(db)


def get_path(name):
    return db.get_key(name, "path")

def get_commit():
    return open('db/ssha.txt', 'r').read()
