import asyncio
from telethon.tl.types import InputStickerSetID, InputStickerSetShortName
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.errors.rpcerrorlist import BadRequestError
from telethon import events, functions, types
from userbot import bot, CMD_HELP


@register(outgoing=True, pattern=r"^.spams(?: |$)(.*)")
async def spams(e):
    reply_msg = await e.get_reply_message()
    if reply_msg and reply_msg.sticker:
        try:
            count = int(e.pattern_match.group(1).strip())
        except ValueError:
            await e.edit("Invalid command format, please provide a number of stickers to spam.")
            return
        if count <= 0:
            await e.edit("Invalid command format, please provide a positive number of stickers to spam.")
            return
        await e.delete()
        for i in range(count):
            await asyncio.sleep(0.2)  # add a 0.2 second delay between each message
            await e.respond(file=reply_msg.sticker, reply_to=reply_msg, supports_streaming=True)
    elif reply_msg and reply_msg.gif:
        try:
            count = int(e.pattern_match.group(1).strip())
        except ValueError:
            await e.edit("Invalid command format, please provide a number of gifs to spam.")
            return
        if count <= 0:
            await e.edit("Invalid command format, please provide a positive number of gifs to spam.")
            return
        await e.delete()
        for i in range(count):
            await asyncio.sleep(0.2)  # add a 0.2 second delay between each message
            await e.respond(file=reply_msg.gif, reply_to=reply_msg)
    else:
        await e.edit("Invalid command format, please reply to a sticker or gif to spam.")


CMD_HELP.update({
    "spams": ".spams <number of messages>\
    \nUsage: Spams the replied sticker a specified number of times.",
    "spamg": ".spamg <number of messages>\
    \nUsage: Spams the replied gif a specified number of times."
})
