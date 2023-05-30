# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru

import utils
import pyttsx3
import pyautogui
import logging
import os
import markup
import webbrowser
from filters import IsAdmin
from data import bot_settings
from aiogram import Bot, Dispatcher, types, executor

bot = Bot(f"{bot_settings['token']}")
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Bot log")


@dp.message_handler(commands=["start"])
async def start_help_message(message: types.Message):
    await message.reply_photo(photo='https://te.legra.ph/file/c17dd46d43541e06cb66f.jpg', caption="<b>🌘 Hi, you can control your computer with this bot\n❓ Do you want the same bot for yourself?\n\n<a href='https://github.com/AmoreForever/pc-controller-bot'>🌍 Repo of this bot</a></b>", parse_mode='HTML')


@dp.message_handler(IsAdmin(), commands="open_link")
async def open_link(message: types.Message):
    args = message.get_args()
    await message.delete()
    webbrowser.open(args, new=0, autoraise=True)
    await message.answer(f"<i>Link going to open.\nLink: <code>{args}</code></i>", parse_mode='html')


@dp.message_handler(IsAdmin(), commands="control")
async def control(message: types.Message):
    await message.answer(
        "<i>🔰 Here you can control your computer</i>",
        parse_mode="html",
        reply_markup=markup.settings(),
    )

@dp.message_handler(IsAdmin(), commands='type')
async def type_text(message: types.Message):
    args = message.get_args()
    try:
        pyautogui.typewrite(str(args))
        await message.answer(text=f"<i>Are you sure you want to send a text: <code>{args}</code></i>", parse_mode='html', reply_markup=markup.enter_or_delete('type'))
    except Exception  as e:
        await message.answer("<b>Please select a place with the mouse where I should write</b>", parse_mode='html')

@dp.message_handler(IsAdmin(), commands="play_yt")
async def play_yt(message: types.Message):
    await message.delete()
    await utils.play_youtube_video(message.get_args())
    await message.answer(f"<i>Video going to open.\nLink: <code>{message.get_args()}</code></i>", parse_mode='html')


@dp.message_handler(IsAdmin(), commands="say")
async def say_message(message: types.Message):
    args = message.get_args()
    engine = pyttsx3.init()
    engine.say(args)
    engine.runAndWait()
    engine.stop()
    await message.delete()


@dp.callback_query_handler(IsAdmin())
async def callbacks(call: types.CallbackQuery):
    if call.data == "screenshot":
        await utils.screenshot()
        await call.message.answer_photo(open("s.png", "rb"), caption="Your monitor screenshot")
        os.remove('s.png')
    if call.data == "home":
        await call.message.edit_text(
        "<i>🔰 Here you can control your computer</i>",
        parse_mode="html",
        reply_markup=markup.settings(),
    )
    if call.data == "close":
        await call.message.delete()
    if call.data == "set-br":
        await call.message.edit_text(
            "🔅 <i>Here you can controll your pc brightness</i>",
            reply_markup=markup.brightness(),
            parse_mode="html",
        )
    if call.data == "set-vol":
        await call.message.edit_text(
            "🔊 <i>Here you can controll your pc volume</i>",
            reply_markup=markup.volume(),
            parse_mode="html",
        )
    if call.data == "shutdown":
        await call.message.edit_text(
            "❔ <i>Are you sure you want to turn off your computer?</i>",
            reply_markup=markup.confirmation("shutdown"),
            parse_mode="html",
        )
    if call.data == "restart":
        await call.message.edit_text(
            "❔ <i>Are you sure you want to restart your computer?</i>",
            reply_markup=markup.confirmation("restart"),
            parse_mode="html",
        )
    if call.data == "lock":
        await call.message.edit_text(
            "❔ <i>Are you sure you want to lock your computer?</i>",
            reply_markup=markup.confirmation("lock"),
            parse_mode="html",
        )
    if call.data == "delete":
        await call.message.edit_text('<i>The text was successfully deleted</i>', parse_mode='html')
        await utils.delete_all()
    if "brightness" in call.data:
        ind = call.data.index("-brightness")
        br = call.data[:ind]
        await utils.brightness(br)
        await call.answer("Done")
    if "volume" in call.data:
        ind = call.data.index("-volume")
        vl = call.data[:ind]
        if vl == 'mute':
            await utils.control_volume(0)
        else:
            await utils.control_volume(int(vl))
        await call.answer("Done")
    if "yes" in call.data:
        ind = call.data.index("-yes")
        comm = call.data[:ind]
        if comm == "lock":
            await call.message.edit_text(
                "<i>Your computer is locking</i>", parse_mode="html"
            )
            await utils.lock_screen()
        elif comm == "restart":
            await call.message.edit_text(
                "<i>Your computer is restarting</i>", parse_mode="html"
            )
            os.system("shutdown /r /t 1")
        elif comm == "shutdown":
            await call.message.edit_text(
                "<i>Your computer is shutting down</i>", parse_mode="html"
            )
            os.system("shutdown /s /t 1")
            
        elif comm == "type":
            await call.message.edit_text(
                "<i>The text was written successfully</i>", parse_mode="html"
            )
            pyautogui.press("enter")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
