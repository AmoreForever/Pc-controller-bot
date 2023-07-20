from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from string import ascii_lowercase, ascii_uppercase, digits, punctuation, ascii_letters
from db import apps as sapps

ru_keyboad_layout = "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,."
ru_keyboad_layout_lower = ru_keyboad_layout.lower()
keyboard_layout = "QWERTYUIOPASDFGHJKLZXCVBNM,."
keyboard_layout_lower = keyboard_layout.lower()


def live():
    markup = InlineKeyboardMarkup(row_width=2)
    start = InlineKeyboardButton(text="▶️ Start", callback_data="start-live")
    stop = InlineKeyboardButton(text="⏹ Stop", callback_data="stop-live")
    markup.add(start, stop)
    return markup
def mouse_control():
    markup = InlineKeyboardMarkup(row_width=3)
    none_keyb = InlineKeyboardButton(text="▪", callback_data='None')
    up = InlineKeyboardButton(text="⬆️", callback_data="up-mouse")
    press = InlineKeyboardButton(text="🖱", callback_data="press-mouse")
    down = InlineKeyboardButton(text="⬇️", callback_data="down-mouse")
    left = InlineKeyboardButton(text="⬅️", callback_data="left-mouse")
    right = InlineKeyboardButton(text="➡️", callback_data="right-mouse")
    markup.add(none_keyb, up, none_keyb)
    markup.add(left, press, right)
    markup.add(none_keyb, down, none_keyb)
    return markup

def digits_keyboard():
    buttons = []
    markup = InlineKeyboardMarkup(row_width=10)
    for item in digits:
        button_text = f"{item}"
        button = InlineKeyboardButton(button_text, callback_data=f"{item}-keyb_typing")
        buttons.append(button)
    ascii = InlineKeyboardButton(text="🔠 ASCII", callback_data="ascii-keyboard")
    backspace = InlineKeyboardButton(text="◀️ Backspace", callback_data="backspace-keyb_typing")
    punctuation = InlineKeyboardButton(text="🔡 Punctuation", callback_data="punctuation-keyboard")
    markup.add(ascii, punctuation)
    markup.add(*buttons)
    markup.add(backspace)
    return markup

def punctuation_keyboard():
    buttons = []
    markup = InlineKeyboardMarkup(row_width=10)
    for item in punctuation:
        button_text = f"{item}"
        button = InlineKeyboardButton(button_text, callback_data=f"{item}-keyb_typing")
        buttons.append(button)
    backspace = InlineKeyboardButton(text="◀️ Backspace", callback_data="backspace-keyb_typing")
    ascii = InlineKeyboardButton(text="🔠 ASCII", callback_data="ascii-keyboard")
    digits = InlineKeyboardButton(text="🔢 Digits", callback_data="digits-keyboard")
    markup.add(digits, ascii)
    markup.add(*buttons)
    markup.add(backspace)
    return markup

def ru_keyboard():
    buttons = []
    markup = InlineKeyboardMarkup(row_width=8)
    for item in ru_keyboad_layout:
        button_text = f"{item}"
        button = InlineKeyboardButton(button_text, callback_data=f"{item}-keyb_typing")
        buttons.append(button)
    to_low = InlineKeyboardButton(text="🔽 To Lower", callback_data="ru-shiftlow")
    backspace = InlineKeyboardButton(text="◀️ Backspace", callback_data="backspace-keyb_typing")
    lang = InlineKeyboardButton(text="🇬🇧 Lang", callback_data="en-lang")
    digits = InlineKeyboardButton(text="🔢 Digits", callback_data="digits-keyboard")
    punctuation = InlineKeyboardButton(text="🔡 Punctuation", callback_data="punctuation-keyboard")
    markup.add(digits, punctuation)
    markup.add(*buttons)
    markup.add(lang, to_low, backspace)
    return markup

def ru_lowercase_keyboard():
    buttons = []
    markup = InlineKeyboardMarkup(row_width=8)
    for item in ru_keyboad_layout_lower:
        button_text = f"{item}"
        button = InlineKeyboardButton(button_text, callback_data=f"{item}-keyb_typing")
        buttons.append(button)
    to_up = InlineKeyboardButton(text="🔼 To Upper", callback_data="ru-shiftup")
    backspace = InlineKeyboardButton(text="◀️ Backspace", callback_data="backspace-keyb_typing")
    lang = InlineKeyboardButton(text="🇬🇧 Lang", callback_data="en-lang")
    digits = InlineKeyboardButton(text="🔢 Digits", callback_data="digits-keyboard")
    punctuation = InlineKeyboardButton(text="🔡 Punctuation", callback_data="punctuation-keyboard")
    markup.add(digits, punctuation)
    markup.add(*buttons)
    markup.add(lang, to_up, backspace)
    return markup

def ascii_lowercase_keyboard():
    buttons = []
    markup = InlineKeyboardMarkup(row_width=8)
    for item in keyboard_layout_lower:
        button_text = f"{item}"
        button = InlineKeyboardButton(button_text, callback_data=f"{item}-keyb_typing")
        buttons.append(button)
    to_up = InlineKeyboardButton(text="🔼 To Upper", callback_data="en-shiftup")
    backspace = InlineKeyboardButton(text="◀️ Backspace", callback_data="backspace-keyb_typing")
    lang = InlineKeyboardButton(text="🇷🇺 Lang", callback_data="ru-lang")
    digits = InlineKeyboardButton(text="🔢 Digits", callback_data="digits-keyboard")
    punctuation = InlineKeyboardButton(text="🔡 Punctuation", callback_data="punctuation-keyboard")
    markup.add(digits, punctuation)
    markup.add(*buttons)
    markup.add(lang, to_up, backspace)
    return markup

def ascii_uppercase_keyboard():
    buttons = []
    markup = InlineKeyboardMarkup(row_width=10)
    for item in keyboard_layout:
        button_text = f"{item}"
        button = InlineKeyboardButton(button_text, callback_data=f"{item}-keyb_typing")
        buttons.append(button)
    to_low = InlineKeyboardButton(text="🔽 To Lower", callback_data="en-shiftlow")
    backspace = InlineKeyboardButton(text="◀️ Backspace", callback_data="backspace-keyb_typing")
    lang = InlineKeyboardButton(text="🇷🇺 Lang", callback_data="ru-lang")
    digits = InlineKeyboardButton(text="🔢 Digits", callback_data="digits-keyboard")
    punctuation = InlineKeyboardButton(text="🔡 Punctuation", callback_data="punctuation-keyboard")
    markup.add(digits, punctuation)
    markup.add(*buttons)
    markup.add(lang, to_low, backspace)
    return markup


def settings():
    markup = InlineKeyboardMarkup()
    shutdown = InlineKeyboardButton(text='🔽 Shutdown', callback_data='shutdown')
    restart = InlineKeyboardButton(text='🔄 Restart', callback_data='restart')
    lock = InlineKeyboardButton(text='🔒 Lock', callback_data='lock')
    brightness = InlineKeyboardButton(text='🔆 Brightness', callback_data='set-br') # type: ignore
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
    apps = sapps.get_apps()
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
    upd = InlineKeyboardButton(text="🔄 Update", callback_data='update')
    can = InlineKeyboardButton(text='🔻 Close', callback_data='close')
    markup.add(upd, can)
    return markup

def log_screen():
    markup = InlineKeyboardMarkup()
    clear = InlineKeyboardButton(text='🗑 Clear', callback_data='clear_logs')
    screen = InlineKeyboardButton(text='📺 Screenshot', callback_data='scrn_logs')
    markup.add(screen, clear)
    return markup