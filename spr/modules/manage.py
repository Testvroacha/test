from os import remove
from pyrogram import filters
from pyrogram.types import Message
import opennsfw2 as n2
from spr import SUDOERS, spr
from spr.utils.mongodb import (disable_nsfw, enable_nsfw, is_nsfw_enabled, enable_admin, disable_admin, is_admin_chat)
from spr.utils.misc import admins, get_file_id

@spr.on_message(
    filters.command("antinsfw") & ~filters.private, group=3
)
async def nsfw_toggle_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "Usage: /antinsfw [on|off]"
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
    if status == "on":
        is_nsfw = await is_nsfw_enabled(chat_id)
        if is_nsfw:
            return await message.reply("Already enabled.")
        await enable_nsfw(chat_id)
        await message.reply_text("Enabled NSFW Detection.")
    elif status == "off":
        is_nsfw = await is_nsfw_enabled(chat_id)
        if not is_nsfw:
            return await message.reply("Already disabled.")
        await disable_nsfw(chat_id)
        await message.reply_text("Disabled NSFW Detection.")
    else:
        await message.reply_text(
            "Unknown Suffix, Use /antinsfw [on|off]"
        )

@spr.on_message(
    filters.command("admindelete") & ~filters.private, group=3
)
async def admin_toggle_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "Usage: /admindelete [on|off]"
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
    if status == "on":
        is_nsfw = await is_admin_chat(chat_id)
        if is_nsfw:
            return await message.reply("Already enabled.")
        await enable_admin(chat_id)
        await message.reply_text("Enabled. Now I will also delete messages of admins which contains NSFW content")
    elif status == "off":
        is_nsfw = await is_admin_chat(chat_id)
        if not is_nsfw:
            return await message.reply("Already disabled.")
        await disable_admin(chat_id)
        await message.reply_text("Disabled. Now I will not delete messages of admins which contains NSFW content")
    else:
        await message.reply_text(
            "Unknown Suffix, Use /admindelete [on|off]"
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
       A, results = n2.predict_video_frames(video_path=file, frame_interval=100000)
    except Exception as e:
        return await m.edit(str(e))
    remove(file)
    hel = max(results)
    result = format(hel, '.0%')
    detected = result.replace("%", "")
    await m.edit(
        f"""
**DETECTION:** {detected}%
"""
    )
