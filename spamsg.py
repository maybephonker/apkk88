import asyncio
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
        sticker = reply_msg.sticker
        if sticker.animated:
            sticker_file = await e.client.download_media(sticker)
        else:
            sticker_file = BytesIO()
            await e.client.download_media(sticker, sticker_file)
            sticker_file.seek(0)
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
            if sticker.animated:
                await e.respond(file=sticker_file, force_document=False)
            else:
                await e.respond(file=sticker_file)
                sticker_file.seek(0)
    else:
        await e.edit("Invalid command format, please reply to a sticker to spam.")

CMD_HELP.update({
    "spams":
    ".spams <number of messages>\
    Usage: Spams the replied sticker a specified number of times."
})

CMD_HELP.update({
    "spamg":
    ".spamg <number of messages>\
    Usage: Spams the replied gif a specified number of times."
})
