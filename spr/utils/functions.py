from time import ctime
from re import compile, search
from spr.utils.mongodb import (disable_nsfw, disable_spam, enable_nsfw,
                          enable_spam, is_nsfw_enabled,
                          is_spam_enabled, del_anti_func, set_anti_func, get_anti_func)
from pyrogram.errors import (ChatAdminRequired, ChatWriteForbidden,
                             UserAdminInvalid)
from pyrogram.types import Message
from spr import NSFW_LOG_CHANNEL, SPAM_LOG_CHANNEL, spr
from spr.core import ikb
from spr.utils.mongodb import get_served_users, is_served_user, add_served_user, get_served_chats, add_served_chat, remove_served_chat, is_served_chat, add_gban_user, is_gbanned_user, remove_gban_user, black_chat, blacklisted_chats, white_chat, is_black_chat


class REGEXES:
    arab = compile('[\u0627-\u064a]')
    chinese = compile('[\u4e00-\u9fff]')
    japanese = compile('[(\u30A0-\u30FF|\u3040-\u309Fー|\u4E00-\u9FFF)]')
    sinhala = compile('[\u0D80-\u0DFF]')
    tamil = compile('[\u0B02-\u0DFF]')
    cyrillic = compile('[\u0400-\u04FF]')


def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


FORM_AND_REGEXES = {
    "ar": [REGEXES.arab, "arabic"],
    "zh": [REGEXES.chinese, "chinese"],
    "jp": [REGEXES.japanese, "japanese"],
    "rs": [REGEXES.cyrillic, "russian"],
    "si": [REGEXES.sinhala, "sinhala"],
    "ta": [REGEXES.tamil, "Tamil"],
}

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
    is_spam: string,
):
    info = await delete_get_info(message)
    if not info:
        return
    msg = f"""
🚨 **SPAM ALERT**  🚔
{info}
**Spam:** {is_spam}
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


async def arab_delete(message, mode):
    # Users list
    users = message.new_chat_members
    chat_id = message.chat.id
    # Obtaining user who sent the message
    tuser = message.from_user
    try:
        mdnrgx = FORM_AND_REGEXES[mode]           
        if message.text:
                  if not tuser:
                      return
                      if search(mdnrgx[0], message.text):
                          await message.delete()
    except:
        pass




