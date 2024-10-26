import importlib
from pyrogram import idle
from uvloop import install
import asyncio
import os
import sys
from pytz import timezone
import croniter
from datetime import datetime
from aiohttp import ClientSession as aiosession

from WhatTheR.modules import ALL_MODULES
from WhatTheR import BOTLOG, LOGGER, app, bots, ids, dB, Client
from config import log_userbot
from WhatTheR.fsup import join

LOOP = asyncio.get_event_loop()

BOT_VER = "3.R.0.R"
PREFIX = [""]
MSG_ON = """<blockquote>Bot aktif sebagai: **{bot_name}** versi {bot_ver}</blockquote>"""

async def load_userbots():
    userbots = dB.get_userbots()  # Mendapatkan semua klien dari database
    for userbot_data in userbots:
        try:
            client = Client(
                name=userbot_data["name"],
                api_id=userbot_data["api_id"],
                api_hash=userbot_data["api_hash"],
                session_string=userbot_data["session_string"],
                plugins=dict(root="WhatTheR/modules")
            )
            bots.append(client)
            print(f"Userbot {userbot_data['name']} started successfully.")
        except Exception as e:
            # Jika sesi direvoke, hapus dari database
            if "session" in str(e).lower():
                dB.remove_ubot(userbot_data["user_id"])  # Ganti remove_userbot dengan remove_ubot
                LOGGER("WhatTheR").error(f"Sesi direvoke untuk userbot {userbot_data['name']}, dihapus dari database.")
            else:
                LOGGER("WhatTheR").error(f"Error saat memulai userbot {userbot_data['name']}: {e}")

async def auto_restart():
    tz = timezone("Asia/Jakarta")
    cron = croniter.croniter("00 00 * * *", datetime.now(tz))
    while True:
        now = datetime.now(tz)
        next_run = cron.get_next(datetime)
        wait_time = (next_run - now).total_seconds()
        await asyncio.sleep(wait_time)
        try:
            await app.send_message(
                log_userbot,
                "<b>Restart Harian...</b>",
            )
        except Exception as e:
            LOGGER("WhatTheR").error(f"Error saat mengirim pesan restart: {e}")
        os.execl(sys.executable, sys.executable, "-m", "WhatTheR")

async def main():
    await app.start()
    print("LOG: Founded Bot token Booting..")
    await asyncio.sleep(1)
    
    for all_module in ALL_MODULES:
        importlib.import_module("WhatTheR.modules" + all_module)
        print(f"Successfully Imported {all_module}")
    
    await load_userbots()

    started_bots = []
    for bot in bots:
        try:
            await bot.start()
            await asyncio.sleep(2)
            ex = await bot.get_me()
            await join(bot)
            await asyncio.sleep(1)
            started_bots.append(f"{ex.first_name} | {ex.id}")
            print(f"Started as {ex.first_name} | {ex.id}")
            ids.append(ex.id)
        except Exception as e:
            # Jika sesi direvoke saat memulai bot
            if "session" in str(e).lower():
                dB.remove_ubot(bot.user_id)  # Hapus bot dari database jika sesi direvoke
                LOGGER("WhatTheR").error(f"Sesi direvoke untuk bot {bot.name}, dihapus dari database.")
            else:
                LOGGER("WhatTheR").error(f"Error saat memulai bot: {e}")

    # Kirim pesan ke BOTLOG dengan semua bot yang berhasil dimulai
    if started_bots:
        try:
            await app.send_message(
                BOTLOG, f"Userbot berhasil dimulai:\n" + "\n".join(started_bots)
            )
        except Exception as e:
            LOGGER("WhatTheR").warning(f"Failed to send userbot startup message: {e}")

    asyncio.create_task(auto_restart())

    await idle()
    await aiosession.close()

if __name__ == "__main__":
    LOGGER("WhatTheR").info("WhatTheR Bot Telah Hidup")
    install()
    LOOP.run_until_complete(main())
