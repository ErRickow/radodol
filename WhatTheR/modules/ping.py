import time
from datetime import datetime
from WhatTheR import *

async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "Jam", "Hari"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time

@ER.UBOT("ping")
async def _(c, m):
    anu = await m.reply("pong")
    await asyncio.sleep(1)
    await anu.edit("ah")

@ER.UBOT("kping")
async def pingme(client: Client, message: Message):
    uptime = await get_readable_time(int(time.time() - StartTime))
    start = datetime.now()
    
    # Menggunakan "WhatTheR" untuk loading
    loading_message = await message.reply_text("**Loading WhatTheR... 0% ▒▒▒▒▒▒▒▒▒▒**")
    
#    try:
 #       await message.delete()
 #   except Exception:
#        pass
    
    # Mengupdate loading progress
    for progress in [20, 40, 60, 80, 100]:
        await loading_message.edit(f"**Loading WhatTheR... {progress}% " + "█" * (progress // 10) + "▒" * (10 - progress // 10) + "**")
        await asyncio.sleep(0.5)  # Tambahkan sedikit jeda agar tidak flood wait

    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await loading_message.edit(
        f"❏ **╰☞ 𝗣𝗢𝗡𝗚™╮**\n"
        f"├• **╰☞** - `%sms`\n"
        f"├• **╰☞ -** `{uptime}` \n"
        f"└• **╰☞:** {client.me.mention}" % (duration)
    )
