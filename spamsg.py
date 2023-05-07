import asyncio
from telethon.tl.types import InputStickerSetID, InputStickerSetShortName
from telethon.tl.functions.messages import GetStickerSetRequest
from userbot import CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.spams")
async def spam_sticker(event):
    if not event.is_reply:
        return await event.edit("Please reply to a sticker to spam.")

    reply_msg = await event.get_reply_message()
    if not reply_msg.sticker:
        return await event.edit("Invalid command format, please reply to a sticker to spam.")

    stickerset_attr = reply_msg.sticker.attributes[1]
    stickerset = await event.client(
        GetStickerSetRequest(
            stickerset=InputStickerSetShortName(
                stickerset_attr.short_name
            )
        )
    )

    while True:
        await event.client.send_file(event.chat_id, reply_msg.sticker)
        await asyncio.sleep(0.2)

@register(outgoing=True, pattern="^.spamg")
async def spam_gif(event):
    if not event.is_reply:
        return await event.edit("Please reply to a GIF to spam.")

    reply_msg = await event.get_reply_message()
    if not reply_msg.document or not reply_msg.document.mime_type.startswith("video/"):
        return await event.edit("Invalid command format, please reply to a GIF to spam.")

    stickerset_attr = reply_msg.document.attributes[1]
    stickerset = await event.client(
        GetStickerSetRequest(
            stickerset=InputStickerSetID(
                id=stickerset_attr.stickerset.id,
                access_hash=stickerset_attr.stickerset.access_hash
            )
        )
    )

    while True:
        await event.client.send_file(event.chat_id, reply_msg.document)
        await asyncio.sleep(0.2)

CMD_HELP.update({
    "spamsticker":
    ".spams\
\nUsage: Reply to a sticker with .spams to spam it in the chat.\
\n\n.spamg\
\nUsage: Reply to a GIF with .spamg to spam it in the chat."
})
