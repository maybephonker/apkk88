import asyncio
from telethon.tl.types import InputStickerSetID, InputStickerSetShortName
from telethon.tl.functions.messages import GetStickerSetRequest
from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.spamg(?: |$)(.*)")
async def spamg(e):
    reply_msg = await e.get_reply_message()
    if reply_msg and reply_msg.gif:
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
            await e.respond(file=reply_msg.gif)
    else:
        await e.edit("Invalid command format, please reply to a gif to spam.")

@register(outgoing=True, pattern="^.spams(?: |$)(.*)")
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
        if not reply_msg.sticker.set_id:
            await e.edit("Invalid command format, please reply to a sticker from a sticker set to spam.")
            return
        sticker_set = await e.client(GetStickerSetRequest(InputStickerSetID(reply_msg.sticker.set_id)))
        is_animated = isinstance(reply_msg.sticker, reply_msg.sticker.TGSSticker)
        file = sticker_set.documents[reply_msg.sticker.documents[0].id - 1].document if not is_animated else reply_msg.sticker
        await e.delete()
        for i in range(count):
            await asyncio.sleep(0.2)  # add a 0.2 second delay between each message
            await e.respond(file=file)
    else:
        await e.edit("Invalid command format, please reply to a sticker to spam.")

CMD_HELP.update({
    "spamg":
    ".spamg <number of messages>\
    Usage: Spams the replied gif a specified number of times.",
    "spams":
    ".spams <number of messages>\
    Usage: Spams the replied sticker a specified number of times."
})
