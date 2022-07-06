import os

from pyrogram import filters
from pyrogram.types import Message

from spr import SUDOERS, arq, spr
from spr.utils.db import (add_chat, add_user, chat_exists,
                          is_chat_blacklisted, is_nsfw_downvoted,
                          is_nsfw_enabled, is_spam_enabled,
                          is_user_blacklisted, update_spam_data,
                          user_exists)
from spr.utils.mongodb import get_served_users, is_served_user, add_served_user, get_served_chats, add_served_chat, remove_served_chat, is_served_chat, add_gban_user, is_gbanned_user, remove_gban_user, black_chat, blacklisted_chats, white_chat, is_black_chat
from spr.utils.functions import (delete_nsfw_notify,
                                 delete_spam_notify, kick_user_notify, get_user_info)
from spr.utils.misc import admins, get_file_id, get_file_unique_id


@spr.on_message(
    (
        filters.document
        | filters.photo
        | filters.sticker
        | filters.animation
        | filters.video
        | filters.text
    )
)
async def message_watcher(_, message: Message):
    user_id = None
    chat_id = None

    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id
        if not chat_exists(chat_id):
            if not await is_served_chat(chat_id):
               add_chat(chat_id)
               await add_served_chat(chat_id)
            if chat_id in await blacklisted_chats():
                 await spr.leave_chat(chat_id)

    if message.from_user:
        if message.from_user.id:
            user_id = message.from_user.id
            if not user_exists(user_id):
                is_served = await is_served_user(user_id)
        if not is_served:
                add_user(user_id)
                await add_served_user(user_id)
                is_gbanned = await is_gbanned_user(user_id)                  
                if is_gbanned:                                  
                        if user_id not in (await admins(chat_id)):                            
                           await spr.ban_chat_member(
            message.chat.id, message.from_user.id
        )
    except (ChatAdminRequired, UserAdminInvalid):
        try:
            return await message.reply_text(
                "I don't have enough permission to ban "
                + "this user who is Blacklisted and Flagged as Spammer."
            )
        except ChatWriteForbidden:
            return await spr.leave_chat(message.chat.id)
    info = await get_user_info(message)
    msg = f"""
🚨 **SPAMMER ALERT**  🚔
{info}
__User has been banned__
"""
    await spr.send_message(message.chat.id, msg)

    if not chat_id or not user_id:
        return

    file_id = get_file_id(message)
    file_unique_id = get_file_unique_id(message)
    if file_id and file_unique_id:
        if user_id in SUDOERS or user_id in (await admins(chat_id)):
            return
        file = await spr.download_media(file_id)
        try:
            resp = await arq.nsfw_scan(file=file)
        except Exception:
            try:
                return os.remove(file)
            except Exception:
                return
        os.remove(file)
        if resp.ok:
            if resp.result.is_nsfw:
                if is_nsfw_enabled(chat_id):
                    return await delete_nsfw_notify(
                        message, resp.result
                    )

    text = message.text or message.caption
    if not text:
        return
    resp = await arq.nlp(text)
    if not resp.ok:
        return
    result = resp.result[0]
    if not result.is_spam:
        return
    if not is_spam_enabled(chat_id):
        return
    if user_id in SUDOERS or user_id in (await admins(chat_id)):
        return
    await delete_spam_notify(message, result.spam_probability)
