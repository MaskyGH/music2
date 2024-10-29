import asyncio

from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

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
        if message.chat.id not in (LOGGER_ID, *await get_acc_group()):
            return await message.reply("Maaf group ini tidak memiliki acces untuk menggunakan bot ini!\nsilahkan hubungin @Mymasky untuk meminta acces!")
        
        return await func(client, message, *args, **kwargs)

    return function


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
            return await message.reply("<b>Usage: /command chat_id or @group [days]</b>")


        chat_id = await extract_id(message, input_identifier)
        acc = await get_acc_group()
        chat = await client.get_chat(chat_id)

        if not chat.id:
            return await message.reply("<b>Invalid chat ID or username provided!</b>")
            
        if chat.id in acc:
            return await message.reply("<b>Group chat is already in the ankes list!</b>")

        await add_acc_group(chat.id)

        if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            response = f"<a href=https://t.me/{chat.username or chat.id}>{chat.title}</a>"
        else:
            response = f"{chat.id}"

        message_content = f"""
<b>Information!</b>

<b>Group:</b> {response}
<b>Reason:</b> Added to acces list
"""
        return await message.reply(message_content)

    except ValueError:
        return await message.reply("<b>Error: Invalid number of days provided. Please provide a valid integer.</b>")
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
            return await message.reply("<b>Usage: /command chat_id or @group [days]</b>")


        chat_id = await extract_id(message, input_identifier)
        acc = await get_acc_group()
        chat = await client.get_chat(chat_id)

        if not chat.id:
            return await message.reply("<b>Invalid chat ID or username provided!</b>")
            
        if chat.id in acc:
            return await message.reply("<b>Group chat is already in the ankes list!</b>")

        await remove_acc_group(chat.id)

        if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            response = f"<a href=https://t.me/{chat.username or chat.id}>{chat.title}</a>"
        else:
            response = f"{chat.id}"

        message_content = f"""
<b>Information!</b>

<b>Group:</b> {response}
<b>Reason:</b> Removed to acces list
"""
        return await message.reply(message_content)

    except ValueError:
        return await message.reply("<b>Error: Invalid number of days provided. Please provide a valid integer.</b>")
    except Exception as e:
        return await message.reply(f"<b>An unexpected error occurred:</b> {str(e)}")


@app.on_message(
    filters.command("listacc")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
async def _(client, message):
    list_acc = await get_acc_group()
    if not list_acc:
        await message.reply("<b>No groups have been added yet.</b>", parse_mode="HTML")
        return
    
    group_list = "<b>List Acc Groups:</b>\n\n"
    for group in list_acc:
        group_list += f"<a href='https://t.me/{group.username or group.id}'>{group.title}</a>\n"
    
    await message.reply(group_list, parse_mode="HTML")
