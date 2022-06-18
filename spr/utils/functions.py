from time import ctime

from pyrogram.errors import (ChatAdminRequired, ChatWriteForbidden,
                             UserAdminInvalid)
from pyrogram.types import Message

from spr import NSFW_LOG_CHANNEL, SPAM_LOG_CHANNEL, spr
from spr.core import ikb
from spr.utils.db import (get_blacklist_event, get_nsfw_count,
                          get_reputation, get_user_trust,
                          increment_nsfw_count, is_user_blacklisted)


async def get_user_info(message):
    user = message.from_user
    trust = get_user_trust(user.id)
    user_ = f"{('@' + user.username) if user.username else user.mention} [`{user.id}`]"
    blacklisted = is_user_blacklisted(user.id)
    reason = None
    if blacklisted:
        reason, time = get_blacklist_event(user.id)
    data = f"""
**User:**
    **Username:** {user_}
    **Trust:** {trust}
    **Spammer:** {True if trust < 50 else False}
    **Reputation:** {get_reputation(user.id)}
    **NSFW Count:** {get_nsfw_count(user.id)}
    **Potential Spammer:** {True if trust < 70 else False}
    **Blacklisted:** {is_user_blacklisted(user.id)}
"""
    data += (
        f"    **Blacklist Reason:** {reason} | {ctime(time)}"
        if reason
        else ""
    )
    return data


async def delete_get_info(message: Message):
    try:
        await message.delete()
    except (ChatAdminRequired, UserAdminInvalid):
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
    result,
):
    info = await delete_get_info(message)
    if not info:
        return
    increment_nsfw_count(message.from_user.id)


async def delete_spam_notify(
    message: Message,
    spam_probability: float,
):
    info = await delete_get_info(message)
    if not info:
        return
 


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
