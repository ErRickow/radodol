from WhatTheR import *

@ER.UBOT("ping")
async def _(c, m):
    await m.reply("pong")