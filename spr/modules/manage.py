from os import remove
from re import compile, search
from pyrogram import filters
from pyrogram.types import Message
from spr import SUDOERS, arq, spr
from spr.utils.mongodb import (disable_nsfw, disable_spam, enable_nsfw,
                          enable_spam, is_nsfw_enabled,
                          is_spam_enabled, del_anti_func, set_anti_func, get_anti_func)
from spr.utils.misc import admins, get_file_id

__MODULE__ = "Manage"
__HELP__ = """
/antinsfw [ENABLE|DISABLE] - Enable or disable NSFW Detection.
/antispam [ENABLE|DISABLE] - Enable or disable Spam Detection.

/nsfwscan - Classify a media.
/spamscan - Get Spam predictions of replied message.
"""

def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


@spr.on_message(
    filters.command("antinsfw") & ~filters.private, group=3
)
async def nsfw_toggle_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "Usage: /antinsfw [ENABLE|DISABLE]"
        )
    if message.from_user:
        user = message.from_user
        chat_id = message.chat.id
        if user.id not in SUDOERS and user.id not in (
            await admins(chat_id)
        ):
            return await message.reply_text(
                "You don't have enough permissions"
            )
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status == "enable":
        is_nsfw = await is_nsfw_enabled(chat_id)
        if is_nsfw:
            return await message.reply("Already enabled.")
        await enable_nsfw(chat_id)
        await message.reply_text("Enabled NSFW Detection.")
    elif status == "disable":
        is_nsfw = await is_nsfw_enabled(chat_id)
        if not is_nsfw:
            return await message.reply("Already disabled.")
        await disable_nsfw(chat_id)
        await message.reply_text("Disabled NSFW Detection.")
    else:
        await message.reply_text(
            "Unknown Suffix, Use /antinsfw [ENABLE|DISABLE]"
        )


@spr.on_message(
    filters.command("antispam") & ~filters.private, group=3
)
async def spam_toggle_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "Usage: /antispam [ENABLE|DISABLE]"
        )
    if message.from_user:
        user = message.from_user
        chat_id = message.chat.id
        if user.id not in SUDOERS and user.id not in (
            await admins(chat_id)
        ):
            return await message.reply_text(
                "You don't have enough permissions"
            )
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status == "enable":
        is_spam = await is_spam_enabled(chat_id)
        if is_spam:
            return await message.reply("Already enabled.")
        await enable_spam(chat_id)
        await message.reply_text("Enabled Spam Detection.")
    elif status == "disable":
        is_spam = await is_spam_enabled(chat_id)
        if not is_spam:
            return await message.reply("Already disabled.")
        await disable_spam(chat_id)
        await message.reply_text("Disabled Spam Detection.")
    else:
        await message.reply_text(
            "Unknown Suffix, Use /antispam [ENABLE|DISABLE]"
        )


@spr.on_message(
    filters.command("antiarab") & ~filters.private, group=3
)
async def arab_toggle_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "Usage: /antiarab [ENABLE|DISABLE]"
        )
    if message.from_user:
        user = message.from_user
        chat_id = message.chat.id
        if user.id not in SUDOERS and user.id not in (
            await admins(chat_id)
        ):
            return await message.reply_text(
                "You don't have enough permissions"
            )
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    args = get_arg(message)
    if not args:
        await message.reply_text(
            "Unknown Suffix, Use /antiarab [ENABLE|DISABLE]"
        )
    lower_args = args.lower()
    if lower_args == "on":
        await set_anti_func(chat_id, "on", "ar")
        await message.reply_text("Enabled Arabic Spam Detection.")
    elif lower_args == "off":
        await del_anti_func(chat_id)       
        await message.reply_text("Disabled Arabic Spam Detection.")
    else:
        await message.reply_text(
            "Unknown Suffix, Use /antiarab [ENABLE|DISABLE]"
        )


@spr.on_message(filters.command("nsfwscan"), group=3)
async def nsfw_scan_command(_, message: Message):
    err = "Reply to an image/document/sticker/animation to scan it."
    if not message.reply_to_message:
        await message.reply_text(err)
        return
    reply = message.reply_to_message
    if (
        not reply.document
        and not reply.photo
        and not reply.sticker
        and not reply.animation
        and not reply.video
    ):
        await message.reply_text(err)
        return
    m = await message.reply_text("Scanning")
    file_id = get_file_id(reply)
    if not file_id:
        return await m.edit("Something went wrong.")
    file = await spr.download_media(file_id)
    try:
        results = await arq.nsfw_scan(file=file)
    except Exception as e:
        return await m.edit(str(e))
    remove(file)
    if not results.ok:
        return await m.edit(results.result)
    results = results.result
    await m.edit(
        f"""
**Neutral:** `{results.neutral} %`
**Porn:** `{results.porn} %`
**Hentai:** `{results.hentai} %`
**Sexy:** `{results.sexy} %`
**Drawings:** `{results.drawings} %`
**NSFW:** `{results.is_nsfw}`
"""
    )


@spr.on_message(filters.command("spamscan"), group=3)
async def scanNLP(_, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to scan it.")
    r = message.reply_to_message
    text = r.text or r.caption
    if not text:
        return await message.reply("Can't scan that")
    data = await arq.nlp(text)
    data = data.result[0]
    msg = f"""
**Is Spam:** {data.is_spam}
**Spam Probability:** {data.spam_probability} %
**Spam:** {data.spam}
**Ham:** {data.ham}
**Profanity:** {data.profanity}
"""
    await message.reply(msg, quote=True)

