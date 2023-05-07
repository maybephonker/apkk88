import asyncio
from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.spams(?: |$)(.*)")
async def spams(e):
    reply_msg = await e.get_reply_message()
    if reply_msg and (reply_msg.media or reply_msg.gif or reply_msg.sticker):
        try:
            count = int(e.pattern_match.group(1).strip())
        except ValueError:
            await e.edit("Invalid command format, please provide a number of messages to spam.")
            return
        if count <= 0:
            await e.edit("Invalid command format, please provide a positive number of messages to spam.")
            return
        await e.delete()
        media = reply_msg.media or reply_msg.gif or reply_msg.sticker
        for i in range(count):
            await asyncio.sleep(0.2)  # add a 0.2 second delay between each message
            await e.respond(file=media)
    else:
        await e.edit("Invalid command format, please reply to a sticker, gif, or photo to spam.")


CMD_HELP.update({
    "spams":
    ".spams <number of messages>\
    Usage: Spams the replied sticker, gif, or photo a specified number of times."
})
