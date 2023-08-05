""" RiZoeLX 2022 © pyRiZoeLX """

from pyrogram.errors import MessageDeleteForbidden, RPCError

async def purge_(RiZoeL, message):

    status_message = await message.reply_text("...", quote=True)
    message_ids = []
    count_del_etion_s = 0

    if message.reply_to_message:
        try:
           for a_s_message_id in range(message.reply_to_message.id, message.id):
              message_ids.append(a_s_message_id)
              if len(message_ids) == 100:
                 count_del_etion_s += await RiZoeL.delete_messages(chat_id=message.chat.id, message_ids=message_ids, revoke=True)
                 message_ids = []
           if len(message_ids) > 0:
              count_del_etion_s += await RiZoeL.delete_messages(chat_id=message.chat.id, message_ids=message_ids, revoke=True)
        except MessageDeleteForbidden:
            await message.reply_text("Cannot delete all messages. The messages may be too old, I might not have delete rights, or this might not be a supergroup.")
            return
        except RPCError as ef:
            await message.reply_text(f"Some error occured! \n\n **Error:** `{ef}`")
            return
    await status_message.edit_text(f"deleted {count_del_etion_s} messages")
    await asyncio.sleep(5)
    await status_message.delete()
