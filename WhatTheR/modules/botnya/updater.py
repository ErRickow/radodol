import os
import sys
import subprocess
import io
from WhatTheR import *

async def send_large_output(message, output):
    with io.BytesIO(str.encode(str(output))) as out_file:
        out_file.name = "update.txt"
        await message.reply_document(document=out_file)

@ER.UBOT("reboot|up", FIL.ME_OWNER)
async def _(c: flyer, m, _):
    return await cb_gitpull2(c, m, _)

@ER.BOT("reboot|up", FIL.ME_OWNER)
async def _(c: bot, m, _):
    return await cb_gitpull2(c, m, _)

async def cb_gitpull(c, m, _):
    out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    if "Already up to date." in str(out):
        return await m.reply(f"<pre>{out}</pre>")
    elif len(str(out)) > 4096:
        await send_large_output(m, out)
    else:
        await m.reply(f"<pre>{out}</pre>")
    await c.shell_exec("pkill -f gunicorn")
    os.execl(sys.executable, sys.executable, "-m", "WhatTheR")

async def cb_gitpull2(c, m, _):
    if m.command[0] == "up":
        eros = await m.reply("<i>Memperbarui... Mohon tunggu...</i>")
        out, err = await c.shell_exec(f"git pull {REPO_URL}")
        
        if "Already up to date." in str(out):
            return await eros.edit(f"<pre>Sudah versi terbaru!\n{out}</pre>")
        
        elif len(str(out)) > 4096:
            await send_large_output(m, out)
        else:
            msg = f"<pre>{out}</pre>"
        
        try:
            await c.shell_exec("pkill -f gunicorn")
            msg += f"\n<i><b>Gunicorn berhasil dimatikan!</i></b>\n"
        except Exception as e:
            return await eros.edit(f"Gagal memperbarui userbot: {str(e)}")

        await eros.edit(
            f"<b>Userbot berhasil diperbarui!</b>\n" + msg
        )
        
        os.execl(sys.executable, sys.executable, "-m", "WhatTheR")
    
    elif m.command[0] == "reboot":
        await c.shell_exec("pkill -f gunicorn")
        await m.reply(
            "<b>Gunicorn berhasil dihentikan. Mencoba merestart Userbot!</b>"
        )
        os.execl(sys.executable, sys.executable, "-m", "WhatTheR")
