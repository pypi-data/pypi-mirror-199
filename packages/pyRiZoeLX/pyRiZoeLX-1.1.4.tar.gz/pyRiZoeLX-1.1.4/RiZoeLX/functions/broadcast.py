"""
   © RiZoeLX
   SpamX - 2022
   Note: function is only for ID not for Bots!
"""


async def broadcast_(RiZoeL, message):
    ok = message.from_user.id
    txt = ' '.join(message.command[1:])
    if txt:
      msg = str(txt)
    elif message.reply_to_message:
        msg = message.reply_to_message.text.markdown
    else:
        await message.reply_text("Give Message for Broadcast or reply to any msg")
        return

    await message.reply_text("__Broadcasting__")
    err = 0
    dn = 0

    async for cht in RiZoeL.get_dialogs():
          try:
                await RiZoeL.send_message(cht.chat.id, msg, disable_web_page_preview=True)
                dn += 1
                await asyncio.sleep(0.1)
          except Exception as e:
              err += 1 
    return await RiZoeL.send_message(ok, f"**• Broadcast Done** ✅ \n\n Chats: {dn} \n Failed In {err} chats")
