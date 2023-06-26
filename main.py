# █ █ █ █▄▀ ▄▀█ █▀▄▀█ █▀█ █▀█ █ █
# █▀█ █ █ █ █▀█ █ ▀ █ █▄█ █▀▄ █▄█

# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# 👤 https://t.me/hikamoru


import asyncio
import platform
import datetime
import logging
import os
import webbrowser
import aioschedule
import pyttsx3
import pyautogui
import data
import misc.utils as utils
import misc.version as version
import misc.commands as commands
import misc.markup as markup
import pygments
from pygments.formatters import ImageFormatter
from pygments.lexers import Python3Lexer
from db import apps
from db import maindb
from misc.filters import IsAdmin
from aiogram import Bot, Dispatcher, types
from aiogram.utils.exceptions import BadRequest

bot = Bot(f"{data.bot_settings['token']}")
dp = Dispatcher(bot)

is_running = True

logging.basicConfig(
    filename="bot-logs.txt",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

logger = logging.getLogger("Bot")


@dp.message_handler(commands="keyboard")
async def keyboard(message: types.Message):
    await message.answer(
        text="⌨️ Here you can type with your keyboard",
        reply_markup=markup.ascii_lowercase_keyboard(),
    )


@dp.message_handler(commands="mouse")
async def mouse(message: types.Message):
    await message.answer(
        text="🖱 Here you can move your mouse", reply_markup=markup.mouse_control()
    )


@dp.message_handler(IsAdmin(), commands="help")
async def help_message(message: types.Message):
    text = (
        "<b>📚 Help</b>\n\n"
        "<code>/help</code> - Get help\n"
        "<code>/keyboard</code> - Get keyboard\n"
        "<code>/mouse</code> - Get mouse\n"
        "<code>/logs</code> - Get logs\n"
        "<code>/live</code> - live screen shots\n"
        "<code>/restart</code> - Restart the bot\n"
        "<code>/update</code> - Update the bot\n"
        "<code>/control</code> - Displays a menu to control your PC\n"
        "<code>/say</code> - Will he say something\n"
        "<code>/open_link</code>  - Opens the link in the browser\n"
        "<code>/play_yt</code>  - Open YouTuve video in the browser\n"
        "<code>/apps</code> - Opens list of apps\n"
        "<code>/addapp</code> - Add app to fast open\n"
        "<code>/rmapp</code> - Remove app from list\n"
    )
    await message.answer(text, parse_mode="html")


@dp.message_handler(IsAdmin(), commands="restart")
async def restart_cmd(message: types.Message):
    args = message.get_args()
    if args == "-i":
        s = await message.answer(
            "<b>🔄 Your bot going to restart...</b>", parse_mode="html"
        )
        await asyncio.sleep(6)
        await s.edit_text("<b>✅ Your bot restarted</b>", parse_mode="html")
        os.system("python3 main.py")
    if not args:
        await message.answer(
            "❓ <b>Are you sure you want to restart?</b>",
            parse_mode="html",
            reply_markup=markup.confirmation("bot_restart"),
        )


@dp.message_handler(IsAdmin(), commands="update")
async def update_cmd(message: types.Message):
    args = message.get_args()
    if args == "-i":
        s = await message.answer(
            "<b>🔄 Your bot going to update...</b>", parse_mode="html"
        )
        await asyncio.sleep(6)
        await s.edit_text("<b>✅ Your bot updated</b>", parse_mode="html")
        os.system("git pull")
        os.system("python3 main.py")
    if not args:
        await message.answer(
            "❓ <b>Are you sure you want to update?</b>",
            parse_mode="html",
            reply_markup=markup.confirmation("bot_update"),
        )


@dp.message_handler(commands=["start"])
async def start_message(message: types.Message):
    await message.reply_photo(
        photo="https://te.legra.ph/file/c17dd46d43541e06cb66f.jpg",
        caption="<b>🌘 Wassup, you can control your computer with this bot\n❓ Do you want the same bot for yourself?\n\n<a href='https://github.com/AmoreForever/pc-controller-bot'>🌍 Repo of this bot</a></b>",
        parse_mode="HTML",
    )


async def get_log_file():
    file = open("bot.log", "r", encoding="utf-8")
    pygments.highlight(
        file.read(),
        Python3Lexer(),
        ImageFormatter(line_numbers=True),
        "fileScreenshot.png",
    )


@dp.message_handler(IsAdmin(), commands="live")
async def live(message: types.Message):
    await send_live(message.from_user.id)


async def send_live(chat_id: int):
    from random import randint
    co = randint(0, 100000)
    try:
        os.remove("s.png")
        await utils.screenshot()
        a = await bot.send_photo(chat_id ,open("s.png", "rb"), reply_markup=markup.live(), caption=f"📸 Скриншот №{co}")
        os.remove("s.png")
        while is_running:
            await utils.screenshot()
            new_photo = types.InputMediaPhoto(media=open("s.png", "rb"))
            await a.edit_caption(f"📸 Скриншот №{co}")
            await a.edit_media(
                media=new_photo,
                reply_markup=markup.live(),
            )
            os.remove("s.png")
            await asyncio.sleep(0.8)
    except FileNotFoundError:
        await utils.screenshot()
        a = await bot.send_photo(chat_id ,open("s.png", "rb"), reply_markup=markup.live(), caption=f"📸 Скриншот №{co}")
        os.remove("s.png")
        while is_running:
            await utils.screenshot()
            new_photo = types.InputMediaPhoto(media=open("s.png", "rb"))
            await a.edit_caption(f"📸 Скриншот №{co}")
            await a.edit_media(
                media=new_photo,
                reply_markup=markup.live(),
            )
            os.remove("s.png")
            await asyncio.sleep(0.8)


@dp.message_handler(IsAdmin(), commands="logs")
async def logs(message: types.Message):
    try:
        await message.answer_document(
            document=open("bot.log", "rb"),
            caption="<b>📜 Here are the logs</b>",
            parse_mode="html",
            reply_markup=markup.log_screen(),
        )
    except BadRequest:  # return if file is empty
        await message.answer("<b>📜 Logs are empty</b>", parse_mode="html")


@dp.message_handler(IsAdmin(), commands="open_link")
async def open_link(message: types.Message):
    args = message.get_args()
    await message.delete()
    webbrowser.open(args, new=0, autoraise=True)
    await message.answer(
        f"<i>Link going to open.\nLink: <code>{args}</code></i>", parse_mode="html"
    )


@dp.message_handler(IsAdmin(), commands="control")
async def control(message: types.Message):
    await message.answer(
        "<i>🔰 Here you can control your computer</i>",
        parse_mode="html",
        reply_markup=markup.settings(),
    )


@dp.message_handler(IsAdmin(), commands="apps")
async def open_apps(message: types.Message):
    if not apps.get_apps():
        await message.answer(
            "<b>🧐 It looks like you haven't added any apps yet</b>", parse_mode="HTML"
        )
    else:
        await message.answer(
            "<b>👩‍🎤 Below are your applications that you can open</b>",
            parse_mode="html",
            reply_markup=markup.apps(),
        )


@dp.message_handler(IsAdmin(), commands="type")
async def type_text(message: types.Message):
    args = message.get_args()
    try:
        pyautogui.typewrite(str(args))
        await message.answer(
            text=f"<i>🐱‍👤 Are you sure you want to send a text: <code>{args}</code></i>",
            parse_mode="html",
            reply_markup=markup.enter_or_delete("type"),
        )
    except Exception as e:
        await message.answer(
            "<b>Please select a place with the mouse where I should write</b>",
            parse_mode="html",
        )


@dp.message_handler(IsAdmin(), commands="play_yt")
async def play_yt(message: types.Message):
    await message.delete()
    await utils.play_youtube_video(message.get_args())
    await message.answer(
        f"<i>Video going to open.\nLink: <code>{message.get_args()}</code></i>",
        parse_mode="html",
    )


@dp.message_handler(IsAdmin(), commands="addapp")
async def add_application(message: types.Message):
    args = message.get_args().split(" | ")
    if len(args) < 2:
        text = (
            "<i>⚠️ Specify the arguments correctly</i>\n"
            r"<i>🦮 Here is an example</i>: <code>Telegram | C:\Users\Amore\AppData\Roaming\64Gram Desktop\Telegram.exe</code>"
        )
        await message.answer(text, parse_mode="html")
    if args[0] and args[1]:
        try:
            apps.add_app(path=args[1], name=args[0])
            await message.answer(
                f"👍 <b>The application {args[0]} has been successfully added to the list</b>",
                parse_mode="html",
            )
        except Exception as e:
            await message.answer(f"Error: {e}")


@dp.message_handler(IsAdmin(), commands="rmapp")
async def rm_app(message: types.Message):
    args = message.get_args()
    if args not in apps.get_apps():
        await message.answer(
            "<b>🙅‍♀️ There is no such application in the database</b>",
            parse_mode="html",
        )
    if args in apps.get_apps():
        apps.del_app(args)
        await message.answer(
            "<i>✔️ The application was successfully removed from the list</i>",
            parse_mode="html",
        )


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
    global is_running
    if call.data == "start-live":
        if is_running:
            await call.answer("🤷‍♀️")
            return
        await call.message.delete()
        is_running = True
        await send_live(call.from_user.id)
        await call.message.answer("<i>📹 Live stream started</i>", parse_mode="html")
    if call.data == "stop-live":
        if is_running:
            await call.message.answer(
                "<i>📹 Live stream stopped</i>", parse_mode="html"
            )
            is_running = False
            await call.message.edit_reply_markup(markup.live())
        else:
            await call.answer("🤷‍♀️")
    if "keyboard" in call.data:
        ind = call.data.index("-keyboard")
        type = call.data[:ind]
        if type == "ascii":
            await call.message.edit_reply_markup(markup.ascii_lowercase_keyboard())
        if type == "digits":
            await call.message.edit_reply_markup(markup.digits_keyboard())
        if type == "punctuation":
            await call.message.edit_reply_markup(markup.punctuation_keyboard())
    if "mouse" in call.data:
        ind = call.data.index("-mouse")
        action = call.data[:ind]
        if action == "left":
            await utils.mouse_left()
            await call.answer("👍")
        elif action == "right":
            await utils.mouse_right()
            await call.answer("👍")
        elif action == "up":
            await utils.mouse_down()
            await call.answer("👍")
        elif action == "down":
            await utils.mouse_up()
            await call.answer("👍")
        elif action == "press":
            await utils.mouse_click()
            await call.answer("👍")
    if "lang" in call.data:
        ind = call.data.index("-lang")
        lang = call.data[:ind]
        if lang == "ru":
            await call.message.edit_reply_markup(markup.ru_lowercase_keyboard())
        elif lang == "en":
            await call.message.edit_reply_markup(markup.ascii_lowercase_keyboard())
    if "shiftlow" in call.data:
        ind = call.data.index("-shiftlow")
        lang = call.data[:ind]
        if lang == "ru":
            await call.message.edit_reply_markup(markup.ru_lowercase_keyboard())
        elif lang == "en":
            await call.message.edit_reply_markup(markup.ascii_lowercase_keyboard())
    if "shiftup" in call.data:
        ind = call.data.index("-shiftup")
        lang = call.data[:ind]
        if lang == "ru":
            await call.message.edit_reply_markup(markup.ru_keyboard())
        elif lang == "en":
            await call.message.edit_reply_markup(markup.ascii_uppercase_keyboard())
    if call.data == "shift-low":
        await call.message.edit_reply_markup(markup.ascii_lowercase_keyboard())
    if call.data == "clear_logs":
        await call.message.delete()
        open("bot.log", "w").close()
        await call.message.answer(
            "<i>📜 <b>Logs cleared successfully</b></i>", parse_mode="html"
        )
    if call.data == "scrn_logs":
        await get_log_file()
        await call.message.answer_document(
            open("fileScreenshot.png", "rb"),
            caption="📜 <b>Here are the logs</b>",
            parse_mode="html",
        )
        os.remove("fileScreenshot.png")
    if call.data == "update":
        await call.message.delete()
        s = await call.message.answer(
            "🔄 <b>Your bot is being updated</b>", parse_mode="html"
        )
        maindb.set_on_off("false")
        maindb.set_message_id(s.message_id)
        os.system("git pull && python main.py")
    if call.data == "screenshot":
        await utils.screenshot()
        await call.message.answer_photo(
            open("s.png", "rb"), caption="Your monitor screenshot"
        )
        os.remove("s.png")
    if call.data == "aplications":
        await call.message.edit_text(
            "<b>👩‍🎤 Below are your applications that you can open</b>",
            parse_mode="html",
            reply_markup=markup.apps(),
        )
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
        await call.message.edit_text(
            "<i>The text was successfully deleted</i>", parse_mode="html"
        )
        await utils.delete_all()
    if "keyb_typing" in call.data:
        ind = call.data.index("-keyb_typing")
        text = call.data[:ind]
        await utils.type_text(text)
        await call.answer("👍")
    if "app" in call.data:
        ind = call.data.index("-app")
        app = call.data[:ind]
        get_path = apps.get_path(str(app))
        try:
            utils.open_application(get_path)
            await call.message.edit_text(
                f"<b>💫 The <code>{app}</code> app opens</b>",
                parse_mode="HTML",
                reply_markup=markup.back_apps(),
            )
        except FileNotFoundError:
            await call.message.edit_text(
                "🚫 <b>The file directory is specified incorrectly or it does not exist</b>",
                reply_markup=markup.delete(app),
                parse_mode="html",
            )

    if "rm" in call.data:
        ind = call.data.index("-rm")
        item = call.data[:ind]
        apps.del_app(item)
        await call.message.edit_text(
            "<i>✔️ The application was successfully removed from the list</i>",
            parse_mode="html",
        )
    if "brightness" in call.data:
        ind = call.data.index("-brightness")
        br = call.data[:ind]
        await utils.brightness(br)
        await call.answer("Done")
    if "volume" in call.data:
        ind = call.data.index("-volume")
        vl = call.data[:ind]
        if vl == "mute":
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
        elif comm == "bot_restart":
            d = await call.message.edit_text(
                "<b>🔄 Your bot going to restart...</b>", parse_mode="html"
            )
            await asyncio.sleep(6)
            await d.edit_text("<b>✅ Your bot restarted</b>", parse_mode="html")
            os.system("python3 main.py")

        elif comm == "bot_update":
            d = await call.message.edit_text(
                "<b>🔄 Your bot going to update...</b>", parse_mode="html"
            )
            await asyncio.sleep(6)
            await d.edit_text("<b>✅ Your bot updated</b>", parse_mode="html")
            os.system("git pull")
            os.system("python3 main.py")


async def startup(dp):
    if maindb.get_on_off() == "false":
        await bot.edit_message_text(
            text="✅ <b>Your bot has been successfully updated</b>",
            message_id=maindb.get_message_id(),
            chat_id=data.tg_id,
            parse_mode="html",
        )
        maindb.set_on_off("true")
    if maindb.get_on_off() == "true":
        await dp.bot.send_message(
            data.tg_id,
            text=f"<b>🌑 Bot started and ready to use</b>\n\n<b>⌛ Now: <code>{datetime.datetime.now()}</code></b>",
            parse_mode="HTML",
            disable_notification=True,
        )
    logger.info("- Notification sent to the owner")


async def starts():
    logger.info("- Version: %s", version.version)
    logger.info("- Owner: %s", data.tg_id)
    logger.info("- Number of commands: %s", len(commands.find_commands_in_file()))
    logger.info("- Release: %s %s", platform.system(), platform.release())
    await dp.start_polling(bot)


async def battery():
    if utils.check_battery() <= 20:  # type: ignore
        await bot.send_message(
            data.tg_id,
            text=f"<b>🪫 Your battery is low, please charge it</b>\n\n<b>⌛ Now: <code>{datetime.datetime.now()}</code></b>",
            parse_mode="HTML",
            disable_notification=True,
        )
    await asyncio.sleep(60)


async def got_scheduled():
    aioschedule.every(30).seconds.do(battery)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(2)


async def on_startup():
    asyncio.create_task(got_scheduled())


async def main():
    f2 = loop.create_task(starts())
    f1 = loop.create_task(on_startup())
    f3 = loop.create_task(startup(dp))
    await asyncio.wait([f1, f2, f3])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()