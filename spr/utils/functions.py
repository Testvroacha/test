from time import ctime

from pyrogram.errors import (ChatAdminRequired, ChatWriteForbidden,
                             UserAdminInvalid)
from pyrogram.types import Message

from spr import NSFW_LOG_CHANNEL, SPAM_LOG_CHANNEL, spr
from spr.core import ikb
from spr.utils.mongodb import get_served_users, is_served_user, add_served_user, get_served_chats, add_served_chat, remove_served_chat, is_served_chat, add_gban_user, is_gbanned_user, remove_gban_user, black_chat, blacklisted_chats, white_chat, is_black_chat
from spr.utils.db import (get_blacklist_event, get_nsfw_count,
                          get_reputation, get_user_trust,
                          increment_nsfw_count, is_user_blacklisted)


async def get_user_info(message):
    user = message.from_user
    user_ = f"{('@' + user.username) if user.username else user.mention} [`{user.id}`]"
    is_gbanned = await is_gbanned_user(user.id)
    reason = None
    if is_gbanned:
        reason, time = get_blacklist_event(user.id)
    data = f"""
**User:**
    **Username:** {user_}
    **Spammer:** {is_gbanned}
    **Blacklisted:** {is_gbanned}
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
    msg = f"""
🚨 **NSFW ALERT**  🚔
{info}
**Prediction:**
    **Safe:** `{result.neutral} %`
    **Porn:** `{result.porn} %`
    **Adult:** `{result.sexy} %`
    **Hentai:** `{result.hentai} %`
    **Drawings:** `{result.drawings} %`
"""
    await spr.send_message(message.chat.id, text=msg)
    


async def delete_spam_notify(
    message: Message,
    spam_probability: float,
):
    info = await delete_get_info(message)
    if not info:
        return
    msg = f"""
🚨 **SPAM ALERT**  🚔
{info}
**Spam Probability:** {spam_probability} %

__Message has been deleted__
"""
    content = message.text or message.caption
    content = content[:400] + "..."
    report = f"""
**SPAM DETECTION**
{info}
**Content:**
{content}
    """

    keyb = ikb(
        {
            "Correct (0)": "upvote_spam",
            "Incorrect (0)": "downvote_spam",
            "Chat": "https://t.me/" + (message.chat.username or "spamlogsss/11"),
        },
        2
    )
    m = await spr.send_message(
        SPAM_LOG_CHANNEL,
        report,
        reply_markup=keyb,
        disable_web_page_preview=True,
    )

    keyb = ikb({"View Message": m.link})
    await spr.send_message(
        message.chat.id, text=msg, reply_markup=keyb
    )


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
