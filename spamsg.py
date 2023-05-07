import asyncio
from telethon.tl.types import InputStickerSetID, InputStickerSetShortName
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.errors.rpcerrorlist import BadRequestError
from telethon import events, functions, types
from userbot import bot, CMD_HELP


async def get_sticker_set(sticker):
    if isinstance(sticker, types.MessageMediaDocument):
        return None  # Document media isn't a sticker
    elif isinstance(sticker, types.MessageMediaPhoto):
        return None  # Photo media isn't a sticker either

    # It's a sticker
    try:
        sticker_set = await bot(
            functions.messages.GetStickerSetRequest(
                sticker.sticker_set.id
            )
        )
    except BadRequestError:
        return None  # Sticker set not found
    return sticker_set


@register(outgoing=True, pattern=r"^.spams(?: |$)(\d+)")
async def spams(event):
    """Spam a sticker a specified number of times."""
    count = int(event.pattern_match.group(1).strip())
    reply = await event.get_reply_message()
    if not reply or not reply.sticker:
        return await event.edit("Invalid command format, please reply to a sticker to spam.")

    # Get the full sticker set to determine if it's animated
    sticker_set = await get_sticker_set(reply)
    is_animated = any(s.document.mime_type == "application/x-tgsticker" for s in sticker_set.documents)

    for i in range(count):
        await asyncio.sleep(0.2)  # add a 0.2 second delay between each message
        try:
            await event.respond(file=reply, reply_to=reply, supports_streaming=is_animated)
        except BadRequestError as e:
            if "Too Many Requests: retry after" in str(e):
                await asyncio.sleep(2)
                await event.respond(file=reply, reply_to=reply, supports_streaming=is_animated)
            else:
                raise e


@register(outgoing=True, pattern=r"^.spamg(?: |$)(\d+)")
async def spamg(event):
    """Spam a gif a specified number of times."""
    count = int(event.pattern_match.group(1).strip())
    reply = await event.get_reply_message()
    if not reply or not reply.gif:
        return await event.edit("Invalid command format, please reply to a gif to spam.")

    for i in range(count):
        await asyncio.sleep(0.2)  # add a 0.2 second delay between each message
        try:
            await event.respond(file=reply.gif, reply_to=reply, supports_streaming=True)
        except BadRequestError as e:
            if "Too Many Requests: retry after" in str(e):
                await asyncio.sleep(2)
                await event.respond(file=reply.gif, reply_to=reply, supports_streaming=True)
            else:
                raise e


CMD_HELP.update({
    "spams": ".spams <number of messages>\
    \nUsage: Spams the replied sticker a specified number of times.",
    "spamg": ".spamg <number of messages>\
    \nUsage: Spams the replied gif a specified number of times."
})
