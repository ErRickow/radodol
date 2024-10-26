from pyrogram import filters, Client
from WhatTheR import app
from config import OWNER_ID, USER_ID, PREFIX, log_userbot

class FIL:
    ME = filters.me
    GROUP = filters.group
    PRIVATE = filters.private
    OWNER = filters.user(OWNER_ID)
    SUDO = filters.user(USER_ID)
    ME_GROUP = filters.me & filters.group
    ME_OWNER = filters.me & filters.user(OWNER_ID)
    ME_USER = filters.me & filters.user(USER_ID)

class ER:
    def BOT(command, filter=FIL.PRIVATE):
        def wrapper(func):
            @app.on_message(filters.command(command) & filter)
            async def wrapped_func(client, message):
                try:
                    await func(client, message)
                except Exception as _err:
                    await app.send_message(
                        log_userbot,
                        f"**Error**: `{_err}`\n"
                        f"**File**: `{__file__}`\n"
                        f"**Command**: `{command}`\n"
                        f"**User**: `{message.from_user.id}`"
                    )
            return wrapped_func
        return wrapper

    def UBOT(command, filter=FIL.ME):
        def wrapper(func):
            @Client.on_message(filters.command(command, PREFIX) & filter)
            async def wrapped_func(client, message):
                try:
                    await func(client, message)
                except Exception as _err:
                    await app.send_message(
                        log_userbot,
                        f"**Error**: `{_err}`\n"
                        f"**File**: `{__file__}`\n"
                        f"**Command**: `{command}`\n"
                        f"**User**: `{message.from_user.id}`"
                    )
            return wrapped_func
        return wrapper

    def GC():
        def wrapper(func):
            @Client.on_message(filters.group & filters.incoming & filters.mentioned & ~filters.bot)
            async def wrapped_func(client, message):
                try:
                    await func(client, message)
                except Exception as _err:
                    await app.send_message(
                        log_userbot,
                        f"**Error**: `{_err}`\n"
                        f"**File**: `{__file__}`\n"
                        f"**In Group**: `{message.chat.id}`\n"
                        f"**User**: `{message.from_user.id}`"
                    )
            return wrapped_func
        return wrapper

    def PC():
        def wrapper(func):
            @Client.on_message(filters.private & filters.incoming & ~filters.me & ~filters.bot & ~filters.service)
            async def wrapped_func(client, message):
                try:
                    await func(client, message)
                except Exception as _err:
                    await app.send_message(
                        log_userbot,
                        f"**Error**: `{_err}`\n"
                        f"**File**: `{__file__}`\n"
                        f"**In Private Chat**: `{message.chat.id}`\n"
                        f"**User**: `{message.from_user.id}`"
                    )
            return wrapped_func
        return wrapper

    def INLINE(command):
        def wrapper(func):
            @app.on_inline_query(filters.regex(command))
            async def wrapped_func(client, query):
                try:
                    await func(client, query)
                except Exception as _err:
                    await app.send_message(
                        log_userbot,
                        f"**Error**: `{_err}`\n"
                        f"**File**: `{__file__}`\n"
                        f"**Inline Command**: `{command}`\n"
                        f"**User**: `{query.from_user.id}`"
                    )
            return wrapped_func
        return wrapper

    def CALLBACK(command):
        def wrapper(func):
            @app.on_callback_query(filters.regex(command))
            async def wrapped_func(client, callback):
                try:
                    await func(client, callback)
                except Exception as _err:
                    await app.send_message(
                        log_userbot,
                        f"**Error**: `{_err}`\n"
                        f"**File**: `{__file__}`\n"
                        f"**Callback Command**: `{command}`\n"
                        f"**User**: `{callback.from_user.id}`"
                    )
            return wrapped_func
        return wrapper
