import os
import requests
from pyrogram import filters, enums
from pyrogram.types import Message
from spr import SUDOERS, arq, spr
from spr.utils.mongodb import get_served_users, is_served_user, add_served_user, get_served_chats, add_served_chat, remove_served_chat, is_served_chat, add_gban_user, is_gbanned_user, remove_gban_user, black_chat, blacklisted_chats, white_chat, is_black_chat, is_nsfw_enabled, is_spam_enabled, disable_nsfw, disable_spam, enable_nsfw, enable_spam, del_anti_func, set_anti_func, get_anti_func
from spr.utils.functions import (delete_nsfw_notify,
                                 delete_spam_notify, kick_user_notify, arab_delete)
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

    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        chat_id = message.chat.id    
        is_serve = await is_served_chat(chat_id)
        if not is_serve:
               await add_served_chat(chat_id)
               await enable_nsfw(chat_id)
               await enable_spam(chat_id)
        if chat_id in await blacklisted_chats():
                 await spr.leave_chat(chat_id)

    if message.from_user:
        if message.from_user.id:
            user_id = message.from_user.id
            is_served = await is_served_user(user_id)
        if not is_served:
                await add_served_user(user_id)
                is_gbanned = await is_gbanned_user(user_id)                  
                if is_gbanned:                                  
                        if user_id not in (await admins(chat_id)):                            
                           await kick_user_notify(message)

    if not chat_id or not user_id:
        return

    file_id = get_file_id(message)
    file_unique_id = get_file_unique_id(message)
    if file_id and file_unique_id:
        if user_id in SUDOERS or user_id in (await admins(chat_id)):
            return
        is_gbanned = await is_gbanned_user(user_id)                  
        if is_gbanned:
            await kick_user_notify(message)
        file = await spr.download_media(file_id)
        try:
            data = requests.post(f"https://safoneapi.herokuapp.com/nsfw", files={'image': open(file, 'rb')}).json()
            is_nsfw = data['data']['is_nsfw']
            hentai = data['data']['hentai']
            drawings = data['data']['drawings']
            porn = data['data']['porn']
            sexy = data['data']['sexy']
            neutral = data['data']['neutral']
        except Exception:
            try:
                return os.remove(file)
            except Exception:
                return
        os.remove(file)
        if is_nsfw=="True":
                is_nfw = await is_nsfw_enabled(chat_id)
                if is_nfw:
                    return await delete_nsfw_notify(
                        message, is_nsfw, porn, sexy, hentai, drawings, neutral
                    )

    text = message.text or message.caption
    if not text:
        return
    data = requests.post(f"https://safoneapi.herokuapp.com/spam", json={'text': message.text}).json()
    is_spam = data['data']['is_spam']
    spam_probability = data['data']['spam_probability']
    spam = data['data']['spam']
    ham = data['data']['ham']
    if is_spam=="False":
       return
    is_spm = await is_spam_enabled(chat_id)
    if not is_spm:
        return
    if user_id in SUDOERS or user_id in (await admins(chat_id)):
        return
    await delete_spam_notify(message, spam_probability, is_spam, spam, ham)
