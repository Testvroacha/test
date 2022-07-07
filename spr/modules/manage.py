from os import remove
from re import compile, search
from pyrogram import filters
from pyrogram.types import Message
from spr import SUDOERS, arq, spr, SUDOERS
from spr.utils.mongodb import (disable_nsfw, disable_spam, enable_nsfw,
                          enable_spam, is_nsfw_enabled,
                          is_spam_enabled, enable_arab, disable_arab, is_arab_enabled)
from spr.utils.misc import admins, get_file_id

__MODULE__ = "Manage"
__HELP__ = """
/anti_nsfw [ENABLE|DISABLE] - Enable or disable NSFW Detection.
/anti_spam [ENABLE|DISABLE] - Enable or disable Spam Detection.
/anti_arab [ENABLE|DISABLE] - Enable or disable arabic spam Detection. 
/nsfw_scan - Classify a media.
/spam_scan - Get Spam predictions of replied message.
"""

antifunc_group = 14

class REGEXES:
    arab = compile('[\u0627-\u064a]')



FORM_AND_REGEXES = {
    "ar": [REGEXES.arab, "arabic"],
}



@spr.on_message(
    filters.command("anti_nsfw") & ~filters.private, group=3
)
async def nsfw_toggle_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "Usage: /anti_nsfw [ENABLE|DISABLE]"
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
            "Unknown Suffix, Use /anti_nsfw [ENABLE|DISABLE]"
        )


@spr.on_message(
    filters.command("anti_spam") & ~filters.private, group=3
)
async def spam_toggle_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "Usage: /anti_spam [ENABLE|DISABLE]"
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
            "Unknown Suffix, Use /anti_spam [ENABLE|DISABLE]"
        )


@spr.on_message(
    filters.command("anti_arab") & ~filters.private, group=3
)
async def arab_toggle_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "Usage: /anti_arab [ENABLE|DISABLE]"
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
        is_arab = await is_arab_enabled(chat_id)
        if is_arab:
            return await message.reply("Already enabled.")
        await enable_arab(chat_id)
        await message.reply_text("Enabled Arabic Spam Detection.")
    elif status == "disable":
        is_arab = await is_arab_enabled(chat_id)
        if not is_arab:
            return await message.reply("Already disabled.")
        await disable_arab(chat_id)
        await message.reply_text("Disabled Arabic Spam Detection.")
    else:
        await message.reply_text(
            "Unknown Suffix, Use /anti_arab [ENABLE|DISABLE]"
        )


@spr.on_message(filters.command("nsfw_scan"), group=3)
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


@spr.on_message(filters.command("spam_scan"), group=3)
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


async def arab_delete(message, mode):
    # Users list
    users = message.new_chat_members
    chat_id = message.chat.id
    # Obtaining user who sent the message
    tuser = message.from_user
    try:
        mdnrgx = FORM_AND_REGEXES[mode]
        if users:
            for user in users:           
               if message.text:
                  if not tuser:
                      return
            if tuser.id in SUDOERS or tuser.id in (await admins(chat_id)):
                return
            if search(mdnrgx[0], message.text):
                    await message.delete()
    except:
        pass





@spr.on_message((filters.new_chat_members | filters.text),group=antifunc_group )
async def check_anti_funcs(_, message: Message):
     is_arab = await is_arab_enabled(chat_id)
     if is_arab:
    # Warns or ban the user from the chat
    await arab_delete(message)

