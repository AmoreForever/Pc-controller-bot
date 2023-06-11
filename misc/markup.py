from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db import db

def settings():
    markup = InlineKeyboardMarkup()
    shutdown = InlineKeyboardButton(text='🔽 Shutdown', callback_data='shutdown')
    restart = InlineKeyboardButton(text='🔄 Restart', callback_data='restart')
    lock = InlineKeyboardButton(text='🔒 Lock', callback_data='lock')
    brightness = InlineKeyboardButton(text='🔆 Brightness', callback_data='set-br')
    volume = InlineKeyboardButton(text='🔊 Volume', callback_data='set-vol')
    screen_shot = InlineKeyboardButton(text="📺 Screenshot", callback_data='screenshot')
    markup.add(brightness, volume, screen_shot)
    markup.add(shutdown, restart, lock)
    return markup

def brightness():
    buttons = []
    lvlvs = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    markup = InlineKeyboardMarkup()
    for item in lvlvs:
        button_text = f"▫️ {item}"
        button = InlineKeyboardButton(button_text, callback_data=f"{item}-brightness")
        buttons.append(button)
    markup.add(*buttons)
    home = InlineKeyboardButton(text="🏘 Home",callback_data="home")
    markup.add(home)
    return markup

def apps():
    buttons = []
    apps = db.get_apps()
    markup = InlineKeyboardMarkup()
    for item in apps:
        button_text = f"▫{item}"
        button = InlineKeyboardButton(button_text, callback_data=f"{item}-app")
        buttons.append(button)
    markup.add(*buttons)
    return markup
   
def delete(app):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(f'Delete {app}', callback_data=f'{app}-rm') 
    markup.add(button)
    return markup

def volume():
    buttons = []
    lvlvs = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    markup = InlineKeyboardMarkup()
    for item in lvlvs:
        button_text = f"▫️ {item}"
        button = InlineKeyboardButton(button_text, callback_data=f"{item}-volume")
        buttons.append(button)
    mute = button = InlineKeyboardButton("🔇 Mute", callback_data="mute-volume")
    markup.add(*buttons)
    home = InlineKeyboardButton(text="🏘 Home",callback_data="home")
    markup.add(mute ,home)
    return markup

def back_apps():
    markup = InlineKeyboardMarkup()
    home = InlineKeyboardButton(text="🔙 Back",callback_data="aplications")
    markup.add(home)
    return markup

def confirmation(what):
    markup = InlineKeyboardMarkup()
    yes = InlineKeyboardButton(text='☑️ Yes ', callback_data=f'{what}-yes')
    cancel = InlineKeyboardButton(text='🚫 Cancel', callback_data='close')
    markup.add(yes, cancel)
    home = InlineKeyboardButton(text="🏘 Home",callback_data="home")
    markup.add(home)
    return markup

def enter_or_delete(what):
    markup = InlineKeyboardMarkup()
    yes = InlineKeyboardButton(text='☑️ Yes ', callback_data=f'{what}-yes')
    cancel = InlineKeyboardButton(text='🚫 Delete', callback_data='delete')
    markup.add(yes, cancel)
    home = InlineKeyboardButton(text="🏘 Home",callback_data="home")
    markup.add(home)
    return markup

def update():
    markup = InlineKeyboardMarkup()
    can = InlineKeyboardButton(text='🔻 Close', callback_data='close')
    markup.add(can)
    return markup