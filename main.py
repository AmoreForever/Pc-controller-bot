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
from db import apps
from db import maindb
from misc.filters import IsAdmin
from aiogram import Bot, Dispatcher, types

bot = Bot(f"{data.bot_settings['token']}")
dp = Dispatcher(bot)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
)


@dp.message_handler(IsAdmin(), commands="help")
async def help_message(message: types.Message):
    text = (
        "<code>/control</code> - Displays a menu to control your PC\n"
        "<code>/say</code> - Will he say something\n"
        "<code>/open_link</code>  - Opens the link in the browser\n"
        "<code>/play_yt</code>  - Open YouTuve video in the browser\n"
        "<code>/apps</code> - Opens list of apps\n"
        "<code>/addapp</code> - Add app to fast open\n"
        "<code>/rmapp</code> - Remove app from list\n"
    )
    await message.answer(text, parse_mode="html")


@dp.message_handler(commands=["start"])
async def start_message(message: types.Message):
    await message.reply_photo(
        photo="https://te.legra.ph/file/c17dd46d43541e06cb66f.jpg",
        caption="<b>🌘 Hi, you can control your computer with this bot\n❓ Do you want the same bot for yourself?\n\n<a href='https://github.com/AmoreForever/pc-controller-bot'>🌍 Repo of this bot</a></b>",
        parse_mode="HTML",
    )


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
            text=f"<i>Are you sure you want to send a text: <code>{args}</code></i>",
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
            text=f"<b>🌑 Your PC is turned on and ready to use</b>\n\n<b>⌛ Now: <code>{datetime.datetime.now()}</code></b>",
            parse_mode="HTML",
            disable_notification=True,
        )
    logger.info("- Notification sent to the owner")


async def starts():
    logger.info("- Version: %s", version.version)
    logger.info("- Owner: %s", data.tg_id)
    logger.info("- Last commit: %s", version.get_latest_commit_sha())
    logger.info("- Number of commands: %s", len(commands.find_commands_in_file()))
    logger.info("- Release: %s %s", platform.system(), platform.release())
    await dp.start_polling(bot)


async def checker():
    if version.get_latest_commit_sha() == apps.get_commit():
        return False
    await bot.send_animation(
        chat_id=data.tg_id,
        animation="https://te.legra.ph/file/63663a6f1791dcfe33108.mp4",
        caption=f"<b>🔄 Hooray, a new update has come out, we urgently need to update</b>\n<b>📦 Commit: <a href='https://github.com/AmoreForever/pc-controller-bot/commit/{version.get_latest_commit_sha()}'>{version.get_latest_commit_sha()}</a></b>",
        reply_markup=markup.update(),
        parse_mode="html",
    )
    open("db/ssha.txt", "w").write(version.get_latest_commit_sha())


async def got_scheduled():
    aioschedule.every(60).seconds.do(checker)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(2)


async def on_startup():
    asyncio.create_task(got_scheduled())


async def main():
    f2 = loop.create_task(starts())
    f1 = loop.create_task(on_startup())
    f3 = loop.create_task(startup(dp))
    await asyncio.wait([f2, f1, f3])


try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
except Exception:
    pass
