import asyncio
import re
from importlib import import_module as import_

from pyrogram import filters, idle, enums
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)

from spr import BOT_USERNAME, session, spr
from spr.modules import MODULES
from spr.utils.misc import paginate_modules


HELPABLE = {}


async def main():
    await spr.start()
    # Load all the modules.
    for module in MODULES:
        imported_module = import_(module)
        if (
            hasattr(imported_module, "__MODULE__")
            and imported_module.__MODULE__
        ):
            imported_module.__MODULE__ = imported_module.__MODULE__
            if (
                hasattr(imported_module, "__HELP__")
                and imported_module.__HELP__
            ):
                HELPABLE[
                    imported_module.__MODULE__.lower()
                ] = imported_module
    print("STARTED !")
    loop = asyncio.get_running_loop()
    await idle()
    await session.close()
    await spr.stop()

HELP_1 = """he"""

@spr.on_message(filters.command(["help", "start"]), group=2)
async def help_command(_, message: Message):
    if message.chat.type != enums.ChatType.PRIVATE:
        buttons = [
            [
                InlineKeyboardButton("Pm Me for Help", url=f"https://t.me/{BOT_USERNAME}?start=help"),
            ],
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        return await message.reply("Click Me For Help", reply_markup=reply_markup)
    buttons = [
            [
                InlineKeyboardButton("✚ Add me to your Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=new"),
            ],
            [
                InlineKeyboardButton("📨 Channel", url=f"https://t.me/CheemsUserbot"),
                InlineKeyboardButton("📨 Group", url=f"https://t.me/CheemsBotChat"),
            ],
            [
                InlineKeyboardButton("🗒 Commands", callback_data="help_callback"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    mention = message.from_user.mention
    await message.reply_photo(
        "https://telegra.ph//file/b2e55cb639b2ffe3b990c.jpg",
        caption=f"Hi {mention}, I'm NoNsfwRobot,"
        + "I Can Protect your group from NSFW media using "
        + "machine learning. Choose an option from below.",
        reply_markup=reply_markup,
    )

@spr.on_callback_query(filters.regex("close"))
async def reinfo(_, query: CallbackQuery):
    try:
        await query.message.delete()
        await query.message.reply_to_message.delete()
    except Exception:
        pass

def help_back_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Close", callback_data=f"close"
                ),
            ]
        ]
    )
    return upl

@spr.on_callback_query(filters.regex("help_callback"))
async def helper_cb(_, CallbackQuery):
    keyboard = help_back_markup(_)
    await CallbackQuery.edit_message_text(
            HELP_1, reply_markup=keyboard
        )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
