
from time import ctime
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)

from spr.utils.mongodb import (disable_nsfw, enable_nsfw, is_nsfw_enabled)
from pyrogram.errors import (ChatAdminRequired, ChatWriteForbidden,
                             UserAdminInvalid, MessageDeleteForbidden)
from pyrogram.types import Message
from spr import spr
from spr.utils.mongodb import get_served_users, is_served_user, add_served_user, get_served_chats, add_served_chat, remove_served_chat, is_served_chat, add_gban_user, is_gbanned_user, remove_gban_user, black_chat, blacklisted_chats, white_chat, is_black_chat

async def get_user_info(message):
    user = message.from_user
    user_ = f"{('@' + user.username) if user.username else user.mention} [`{user.id}`]"
    is_gbanned = await is_gbanned_user(user.id)
    reason = None
    data = f"""
**User:**
    **Username:** {user_}
    **Spammer:** {is_gbanned}
    **Blacklisted:** {is_gbanned}
"""
    return data


async def delete_get_info(message: Message):
    try:
        await message.delete()
    except (ChatAdminRequired, UserAdminInvalid, MessageDeleteForbidden):
        try:
            return await message.reply_text(
                "I don't have enough permission to delete "
                + "this message which is Flagged as Spam."
            )
        except ChatWriteForbidden:
            return await spr.leave_chat(message.chat.id)
    return await get_user_info(message)


async def delete_nsfw_notify(
    message: Message,  
    results, 
):
    info = await delete_get_info(message)
    if not info:
        return
    hel = min(results)
    result = format(hel, '.0%')
    msg = f"""
🚨 **NSFW ALERT**  🚔
{info}
**Nsfw Probability:** {result}

__Message has been deleted__
"""
    await spr.send_message(message.chat.id, text=msg)
    

async def kick_user_notify(message: Message):
    try:
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
