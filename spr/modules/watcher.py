import os
from pyrogram import filters, enums
from pyrogram.types import Message
import opennsfw2 as n2
from spr import SUDOERS, spr
from spr.utils.mongodb import get_served_users, is_served_user, add_served_user, get_served_chats, add_served_chat, remove_served_chat, is_served_chat, add_gban_user, is_gbanned_user, remove_gban_user, black_chat, blacklisted_chats, white_chat, is_black_chat, is_nsfw_enabled, enable_nsfw, disable_nsfw, is_admin_chat, save_nsfw
from spr.utils.functions import (delete_nsfw_notify, kick_user_notify)
from spr.utils.misc import admins, get_file_id, get_file_unique_id



@spr.on_message(
    (
        filters.document
        | filters.photo
        | filters.sticker
        | filters.animation
        | filters.video
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
        is_serve = await is_served_chat(chat_id)
        if not is_serve:
               await add_served_chat(chat_id)
        if user_id in SUDOERS:
               return
        is_gbanned = await is_gbanned_user(user_id)                 
        if is_gbanned:
            await kick_user_notify(message)
        file = await spr.download_media(file_id)
        try:
            A, results = n2.predict_video_frames(video_path=file, frame_interval=100000)                        
        except Exception:
            try:
                return os.remove(file)
            except Exception:
                return
        os.remove(file)     
        hel = max(results)
        result = format(hel, '.0%')
        detected = result.replace("%", "")
        if int(detected) > 20:
                is_nfw = await is_nsfw_enabled(chat_id)
                if is_nfw:
                         admin_chat = await is_admin_chat(chat_id)
                         if not admin_chat:                             
                            if user_id not in (await admins(chat_id)):
                               await save_nsfw(user_id)
                               return await delete_nsfw_notify(message, detected)
                         else: 
                            await save_nsfw(user_id)              
                            return await delete_nsfw_notify(message, detected)
    
