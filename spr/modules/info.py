from time import ctime

from pyrogram import filters
from pyrogram.types import (InlineQuery, InlineQueryResultArticle,
                            InputTextMessageContent, Message)
from spr.utils.mongodb import get_served_users, is_served_user, add_served_user, get_served_chats, add_served_chat, remove_served_chat, is_served_chat, add_gban_user, is_gbanned_user, remove_gban_user, black_chat, blacklisted_chats, white_chat, is_black_chat
from spr import SUDOERS, spr
from spr.utils.db import (add_chat, add_user, chat_exists,
                          get_blacklist_event, get_nsfw_count,
                          get_reputation, get_user_trust,
                          is_chat_blacklisted, is_user_blacklisted,
                          user_exists)

__MODULE__ = "Info"
__HELP__ = """
**Get Info About A Chat Or User**

/info [CHAT_ID/Username|USER_ID/Username]

or you can use inline mode >>
@SpamProtection_Bot [CHAT_ID/Username|USER_ID/Username]
"""


async def get_user_info(user):
    try:
        user = await spr.get_users(user)
    except Exception:
        return            
        is_serve = await is_served_user(user.id)
        if not is_serve:
           await add_served_user(user.id)
    is_gbanned = await is_gbanned_user(user.id)
    reason = None
    if is_gbanned:
        data = f"""
**ID:** {user.id}
**DC:** {user.dc_id}
**Username:** {user.username}
**Mention: ** {user.mention("Link")}

**Is Sudo:** {user.id in SUDOERS}
**Spammer:** {is_gbanned}
**Blacklisted:** {is_gbanned}
"""
    data += (
        f"**Blacklist Reason:** {reason} | {ctime(time)}"
        if reason
        else ""
    )
    return data


async def get_chat_info(chat):
    try:
        chat = await spr.get_chat(chat)
    except Exception:
        return
    is_served = await is_served_user(chat.id)
        if not is_served:
           await add_served_chat(chat.id)           
    blackchat = await is_black_chat(chat.id)
    reason = None
    if blackchat:
        data = f"""
**ID:** {chat.id}
**Username:** {chat.username}
**Type:** {chat.type}
**Members:** {chat.members_count}
**Scam:** {chat.is_scam}
**Restricted:** {chat.is_restricted}
**Blacklisted:** {blackchat}
"""
    data += (
        f"**Blacklist Reason:** {reason} | {ctime(time)}"
        if reason
        else ""
    )
    return data


async def get_info(entity):
    user = await get_user_info(entity)
    if user:
        return user
    chat = await get_chat_info(entity)
    return chat


@spr.on_message(filters.command("info"), group=3)
async def info_func(_, message: Message):
    if message.reply_to_message:
        reply = message.reply_to_message
        user = reply.from_user
        entity = user.id or message.chat.id
    elif len(message.command) == 1:
        user = message.from_user
        entity = user.id or message.chat.id
    elif len(message.command) == 2:
        entity = message.text.split(None, 1)[1]
    else:
        return await message.reply_text("Read the help menu")
    entity = await get_info(entity)
    entity = entity or "I haven't seen this chat/user."
    await message.reply_text(entity)


@spr.on_inline_query()
async def inline_info_func(_, query: InlineQuery):
    query_ = query.query.strip()
    entity = await get_info(query_)
    if not entity:
        err = "I haven't seen this user/chat."
        results = [
            InlineQueryResultArticle(
                err,
                input_message_content=InputTextMessageContent(err),
            )
        ]
    else:
        results = [
            InlineQueryResultArticle(
                "Found Entity",
                input_message_content=InputTextMessageContent(entity),
            )
        ]
    await query.answer(results=results, cache_time=3)
