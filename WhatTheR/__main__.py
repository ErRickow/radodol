import importlib
from pyrogram import idle
from uvloop import install
import asyncio
from datetime import datetime

from WhatTheR.modules import ALL_MODULES
from WhatTheR import BOTLOG, LOGGER, LOOP, aiosession, app, bots, ids
from WhatTheR.modules.basic import join
from WhatTheR.helpers.misc import heroku

BOT_VER = "3.R.0.R"
PREFIX = [""]
MSG_ON = """<blockquote>{mention} **AKTIF**
<blockquote>
"""

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
                "<blockquote><b>Restart Daily...</b></blockquote>",
            )
        except:
            pass
        os.execl(sys.executable, sys.executable, "-m", "WhatTheR")


async def main():
    await app.start()
    print("LOG: Founded Bot token Booting..")
    for all_module in ALL_MODULES:
        importlib.import_module("WhatTheR.modules" + all_module)
        print(f"Successfully Imported {all_module} ")
    for bot in bots:
        try:
            await bot.start()
            ex = await bot.get_me()
            await join(bot)
            try:
                await bot.send_message(BOTLOG, MSG_ON.format(BOT_VER, CMD_HANDLER))
            except BaseException:
                pass
            print(f"Started as {ex.first_name} | {ex.id} ")
            ids.append(ex.id)
        except Exception as e:
            print(f"{e}")
    await asyncio.sleep(100)
    await idle()
    await aiosession.close()


if __name__ == "__main__":
    LOGGER("WhatTheR").info("WhatTheR Telah Hidup")
    install()
    heroku()
    LOOP.run_until_complete(main())
