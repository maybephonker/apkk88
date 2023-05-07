import asyncio
import random
from userbot import CMD_HELP
from userbot.events import register


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
        await e.delete()
        for i in range(count):
            await asyncio.sleep(0.2)  # add a 0.2 second delay between each message
            await e.respond(file=reply_msg.sticker)
    else:
        await e.edit("Invalid command format, please reply to a sticker to spam.")


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


@register(outgoing=True, pattern="^.spam(?: |$)(.*)")
async def spam(e):
    reply_msg = await e.get_reply_message()
    if reply_msg and (reply_msg.video or reply_msg.audio or reply_msg.voice or reply_msg.photo or reply_msg.document):
        try:
            count = int(e.pattern_match.group(1).strip())
        except ValueError:
            await e.edit("Invalid command format, please provide a number of media to spam.")
            return
        if count <= 0:
            await e.edit("Invalid command format, please provide a positive number of media to spam.")
            return
        await e.delete()
        delay = 0.2  # default delay time between messages is 0.2 seconds
        if e.pattern_match.group(2):
            try:
                delay = float(e.pattern_match.group(2).strip())
            except ValueError:
                pass
        for i in range(count):
            await asyncio.sleep(delay)
            media_type = random.choice(["video", "audio", "voice", "photo", "document"])  # randomly select media type to spam
            media_file = getattr(reply_msg, media_type)
            await e.respond(file=media_file)
    else:
        await e.edit("Invalid command format, please reply to a media message to spam.")


CMD_HELP.update({
    "spamg":
    ".spamg <number of messages>\
    \nUsage: Spams the replied gif a specified number of times."
})

CMD_HELP.update({
    "spams":
    ".spams <number of messages>\
    \nUsage: Spams the replied sticker a specified number of times."
})
