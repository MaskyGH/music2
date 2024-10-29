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
from config import OWNER_ID



def check_acces(func)
    async def function(client, message):
        anu = await is_acc_group(message.chat.id)

            if not anu:
                return
        
            await func(client, message)

        return function


@app.on_message(
    filters.command("addacc")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
async def _(client, message):
    anu = await message.reply("<b>Processing...</b>")
  
    if len(message.command) > 1:
        input_identifier = message.command[1]
        
        try:
            chat = await client.get_chat(input_identifier)
            if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                txt = f"<b><a href='https://t.me/{chat.username or chat.id}'>{chat.title}</a> has been added to the data acces group!</b>"
                await anu.edit_text(txt, parse_mode="HTML")
                return await add_acc_group(chat.id)
            else:
                await anu.edit_text("<b>This chat is not a group or supergroup.</b>", parse_mode="HTML")
        except Exception as e:
            await anu.edit_text(f"<b>Error: {str(e)}</b>", parse_mode="HTML")
    else:
        await anu.edit_text("<b>Please provide a group identifier.</b>", parse_mode="HTML")


@app.on_message(
    filters.command("dellacc")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot
)
async def _(client, message):
    anu = await message.reply("<b>Processing...</b>")
  
    if len(message.command) > 1:
        input_identifier = message.command[1]
        
        try:
            chat = await client.get_chat(input_identifier)
            if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                txt = f"<b><a href='https://t.me/{chat.username or chat.id}'>{chat.title}</a> has been removed to the data acces group!</b>"
                await anu.edit_text(txt, parse_mode="HTML")
                return await remove_acc_group(chat.id)
            else:
                return await anu.edit_text("<b>This chat is not a group or supergroup.</b>", parse_mode="HTML")
        except Exception as e:
            return await anu.edit_text(f"<b>Error: {str(e)}</b>", parse_mode="HTML")
    else:
        return await anu.edit_text("<b>Please provide a group identifier.</b>", parse_mode="HTML")

async def _(client, message):
    list_acc = await get_acc_group()
    if not list_acc:
        await message.reply("<b>No groups have been added yet.</b>", parse_mode="HTML")
        return
    
    group_list = "<b>List Acc Groups:</b>\n\n"
    for group in list_acc:
        group_list += f"<a href='https://t.me/{group.username or group.id}'>{group.title}</a>\n"
    
    await message.reply(group_list, parse_mode="HTML")
