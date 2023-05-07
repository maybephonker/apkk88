import asyncio
from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.spams(?: |$)(.*)")
async def spams(e):
    reply_msg = await e.get_reply_message()
    if reply_msg and (reply_msg.media or reply_msg.gif):
        try:
            count = int(e.pattern_match.group(1).strip())
        except ValueError:
            await e.edit("Invalid command format, please provide a number of messages to spam.")
            return
        if count <= 0:
            await e.edit("Invalid command format, please provide a positive number of messages to spam.")
            return
        await e.delete()
        media = reply_msg.media or reply_msg.gif
        for i in range(count):
            await asyncio.sleep(1)  # add a 1 second delay between each message
            await e.respond(file=media)
    else:
        await e.edit("Invalid command format, please reply to a sticker or gif to spam.")


CMD_HELP.update({
    "spams":
    ".spams <number of messages>\
    Usage: Spams the replied sticker or gif a specified number of times."
})
