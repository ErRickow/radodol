from WhatTheR import *
from config import OWNER_ID, ALIVE_PIC, log_userbot
from pyrogram import filters
import os
import re
import asyncio
import time
from pyrogram import *
from pyrogram.types import *

PHONE_NUMBER_TEXT = (
    "✘ Heya My Master👋!\n\n✘ I'm Your Assistant?\n\n‣ I can help you to host Your Left Clients.\n\n‣ Repo: github.com/Itz-WhatTheR/WhatTheR-Userbot \n\n‣ This specially for Buzzy People's(lazy)\n\n‣ Now /clone {send your PyroGram String Session}"
)

@ER.BOT("start")
async def hello(client: app, message):
    buttons = [
        [
            InlineKeyboardButton("✘ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ", url="t.me/TheUpdatesChannel"),
        ],
        [
            InlineKeyboardButton("✘ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url="t.me/TheSupportChat"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_photo(message.chat.id, ALIVE_PIC, caption=PHONE_NUMBER_TEXT, reply_markup=reply_markup)

@ER.BOT("clone")
async def clone(bot: app, msg: Message):
    if len(msg.command) < 2:
        await msg.reply("**Usage:**\n\n`/clone <session_string>`\n\nPlease provide your session string.")
        return

    phone = msg.command[1]
    text = await msg.reply("Booting Your Client")
    try:
        await asyncio.sleep(5)
        # Ganti direktori ini sesuai dengan repo Anda
        client = Client(
            name="Melody",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=phone,
            plugins=dict(root="WhatTheR/modules")
        )
        await client.start()
        user = await client.get_me()
        await msg.reply(f"Your Client Has Been Successfully Started as {user.first_name} ✅.")
        await app.send_message(log_userbot, "New Client started")
    except Exception as e:
        await msg.reply(f"**ERROR:** `{str(e)}`\nPress /start to try again.")
