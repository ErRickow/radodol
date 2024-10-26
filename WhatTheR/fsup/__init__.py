import os
import sys
from pyrogram import Client



def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "WhatTheR"])

async def join(client):
    try:
        await client.join_chat("Er_Support_Group")
        await client.join_chat("PamerDong")
        await client.join_chat("ZeebSupport")
 #       await client.join_chat("kynansupport")
    except BaseException:
        pass
