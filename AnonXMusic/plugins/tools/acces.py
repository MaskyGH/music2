import asyncio

from pyrogram import *
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.types import *

from AnonXMusic import app
from AnonXMusic.utils.database import (
    get_acc_group,
    is_acc_group,
    add_acc_group,
    remove_acc_group,
)
from config import OWNER_ID, LOGGER_ID



async def extract_id(message, text):
    def is_int(text):
        try:
            return int(text)
        except ValueError:
            return None

    text = text.strip() if text else ''

    chat_id = is_int(text)
    if chat_id is not None:
        if str(chat_id).startswith('-') or chat_id > 0:
            return chat_id

    app = message._client
    entities = message.entities

    if entities:
        entity = entities[1 if message.text.startswith("/") else 0]
        if entity.type == enums.MessageEntityType.MENTION:
            try:
                user = await app.get_chat(text)
                return user.id
            except Exception:
                return None
        elif entity.type == enums.MessageEntityType.TEXT_MENTION:
            return entity.user.id
            
    if text.startswith('@'):
        try:
            chat = await app.get_chat(text)
            return chat.id
        except Exception:
            return None

    return None


def check_access(func):
    async def function(client, message, *args, **kwargs):
        if message.chat.id not in (LOGGER_ID, *await get_list_vars(client.me.id, "acc_gc")):
            return await message.reply("""
Maaf group ini tidak memiliki acces untuk menggunakan bot ini!
silahkan hubungin Owner untuk meminta acces!
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Masky86", user_id=5312739535),
                    ],
                ]
              )
            )
        
        return await func(client, message, *args, **kwargs)

    return function


async def handle_chat_access(client, message, chat_id, action):
    chat = await client.get_chat(chat_id)

    if not chat:
        return await message.reply("<b>Invalid chat ID or username provided!</b>")
    
    acc = await get_list_vars(client.me.id, "acc_gc")

    if action == "add" and chat.id in acc:
        return await message.reply("<b>Group chat is already in the access list!</b>")
    if action == "remove" and chat.id not in acc:
        return await message.reply("<b>Group chat is not in the access list!</b>")

    if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        response = f"<a href=https://t.me/{chat.username or chat.id}>{chat.title}</a>"
    else:
        response = f"{chat.id}"

    message_content = f"""
<b>Information!</b>

<b>Group:</b> {response}
<b>Reason:</b> {action.capitalize()}ed to access list
"""
    if action == "add":
        await add_list_vars(client.me.id, "acc_gc", chat.id)
    else:
        await remove_list_vars(client.me.id, "acc_gc", chat.id)
    
    return await message.reply(message_content)


@app.on_message(
    filters.command("addacc")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
async def _(client, message):
    try:
        if len(message.command) > 1:
            input_identifier = message.command[1]
        else:
            return await message.reply("<b>Usage: /addacc chat_id or @group</b>")

        chat_id = await extract_id(message, input_identifier)
        return await handle_chat_access(client, message, chat_id, "add")

    except ValueError:
        return await message.reply("<b>Error: Invalid chat ID format. Please provide a valid ID or username.</b>")
    except Exception as e:
        return await message.reply(f"<b>An unexpected error occurred:</b> {str(e)}")


@app.on_message(
    filters.command("dellacc")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
async def _(client, message):
    try:
        if len(message.command) > 1:
            input_identifier = message.command[1]
        else:
            return await message.reply("<b>Usage: /dellacc chat_id or @group</b>")

        chat_id = await extract_id(message, input_identifier)
        return await handle_chat_access(client, message, chat_id, "remove")

    except ValueError:
        return await message.reply("<b>Error: Invalid chat ID format. Please provide a valid ID or username.</b>")
    except Exception as e:
        return await message.reply(f"<b>An unexpected error occurred:</b> {str(e)}")


@app.on_message(
    filters.command("listacc")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
async def _(client, message):
    list_acc = await get_list_vars(client.me.id, "acc_gc")
    if not list_acc:
        await message.reply("<b>No groups have been added yet.</b>")
        return
    
    group_list = "<b>List Acc Groups:</b>\n\n"
    for group_id in list_acc:
        chat = await client.get_chat(group_id)
        if chat:
            group_list += f"<a href='https://t.me/{chat.username or chat.id}'>{chat.title}</a>\n"
    
    await message.reply(group_list)
