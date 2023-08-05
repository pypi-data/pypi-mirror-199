

"""
   Pyrogram Module [Info lf individual user]
   
   from RiZoeL.functions import get_info
   await get_info(bot, message)
"""

from RiZoeLX import *

async def get_info(RiZoeL, message):
   try:
      args = message.text.split(" ", 1)[1].split(" ", 1)
   except IndexError:
      args = None

   if message.reply_to_message and message.reply_to_message.from_user:
      user = message.reply_to_message.from_user

   elif args:
      user_ = args[0]
      if user_.isnumeric():
           user_ = int(user_)
      if not user_:
           await message.reply_text("I don't know who you're talking about, you're going to need to specify a user.!")
           return
      try:
         user = await RiZoeL.get_users(user_)
      except (TypeError, ValueError):
         await message.reply_text("Looks like I don't have control over that user, or the ID isn't a valid one. If you reply to one of their messages, I'll be able to interact with them.")
         return
   else:
      await message.reply_text("I don't know who you're talking about, you're going to need to specify a user...!")
      return

   info = "User Info! \n\n"
   info += f"First Name: {user.first_name} \n"
   if user.last_name:
     info += f"Last Name: {user.last_name} \n"
   info += f"User ID: {user.id} \n"
   if user.username:
     info += f"Username: @{user.username} \n"
   info += "permit link: {} \n"
   if int(user.id) in Devs:
     info += f"Owner of @RiZoeLX 🔱\n"
   await message.reply_text(info, disable_web_page_preview=True)


"""
   Pyrogram Module [Info lf individual user]
   
   from RiZoeL.functions import get_id
   await get_id(bot, message)
"""

async def get_id(RiZoeL, message):
    chat = message.chat
    your_id = message.from_user.id
    reply = message.reply_to_message
    text = f"**Your ID:** `{your_id}`\n"
    text += f"**Chat ID:** `{chat.id}`\n\n"

    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user = await RiZoeL.get_users(split)
            text += f"{user.first_name}'s ID: `{user.id}`\n"

        except Exception:
            return await message.reply_text("This user doesn't exist.", quote=True)

    if not getattr(reply, "empty", True) and not message.forward_from_chat and not reply.sender_chat:
      try:
        user = await RiZoeL.get_users(reply.from_user.id)
        text += f"**{user.first_name}'s ID:** `{reply.from_user.id}` \n\n"
      except:
        text += f"**Replied User ID:** `{reply.from_user.id}` \n\n"

    if reply and reply.forward_from_chat:
        text += f"The forwarded channel, {reply.forward_from_chat.title}, has an id of `{reply.forward_from_chat.id}`\n\n"
        print(reply.forward_from_chat)

    if reply and reply.sender_chat:
        text += f"ID of the replied chat/channel, is `{reply.sender_chat.id}`"
        print(reply.sender_chat)

    await message.reply_text(
       text,
       disable_web_page_preview=True,
    )
