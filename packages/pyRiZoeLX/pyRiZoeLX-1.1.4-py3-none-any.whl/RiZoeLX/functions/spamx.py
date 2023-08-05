"""
   © RiZoeLX - SpamX
   functions of RiZoeLX/SpamX
"""

from RiZoeLX.developers import *
from RiZoeLX.data import *
import random, asyncio, re

async def dor(message, editor, text):
   try:
     await editor.edit_text(text)
   except:
     await editor.delete()
     await message.reply_text(text)

res_devs = "RiZoeL|Mahipal|Akash|TheRiZoeL|TheVenomXD"
res_grps = [1517994352, 1789859817, -1001321613309, 1321613309, 1001749467927, 1749467927]


""" Get User with Reason! """
async def user_reason(RiZoeL, message, Owner, Sudos):
    try:
       args = message.text.split(" ", 1)[1].split(" ", 1)
    except IndexError:
       args = None

    if message.reply_to_message and message.reply_to_message.from_user:
       user = message.reply_to_message.from_user
       reason =  "".join(args) if args else ""

    elif args:
       reason = None
       user_ = args[0]
       if len(args) == 2:
           reason = args[1]
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

    if int(user.id) in Devs:
        await message.reply_text(f"{user.mention} is Owner/Dev of @RiZoeLX")
        return
    if int(user.id) == Owner:
        await message.reply_text(f"{user.mention} is owner of these bots!")
        return
    if int(user.id) in Sudos:
      if message.from_user.id != Owner:
         await message.reply_text(f"{user.mention} is Sudo User!")
         return

    return user, reason

async def user_only(RiZoeL, message, Owner, Sudos):
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

    if int(user.id) in Devs:
        await message.reply_text(f"{user.mention} is Owner/Dev of @RiZoeLX")
        return
    if int(user.id) == Owner:
        await message.reply_text(f"{user.mention} is owner of these bots!")
        return
    if int(user.id) in Sudos:
      if message.from_user.id != Owner:
         await message.reply_text(f"{user.mention} is Sudo User!")
         return

    return user

"""Spam functions"""
async def start_raid(RiZoeL, message, counts, user):
   chat = message.chat
   if chat.id in res_grps:
      await message.reply_text("**Sorry!** I can't raid here.")
      return
   if int(user.id) in Devs:
      await message.reply_text("I can't raid on @RiZoeLX's Owner")
      return
   for _ in range(counts):
      raid = random.choice(raids.raid)
      await RiZoeL.send_message(chat.id, f"{user.mention} {raid}")
      await asyncio.sleep(0.3) 

async def start_spam(RiZoeL, message, counts, spam_text):
   chat = message.chat
   if chat.id in res_grps:
      await message.reply_text("**Sorry!** I can't spam here.")
      return
   if re.search(res_devs.lower(), spam_text.lower()):
      await message.reply_text("**Error!**")
      return
   for _ in range(counts):
      await RiZoeL.send_message(chat.id, str(spam_text))
      await asyncio.sleep(0.3)

async def start_dm_raid(RiZoeL, message, counts, user):
   if int(user) in Devs:
      await message.reply_text("User is Dev of SpamX:)")
      return 
   for _ in range(counts):
      raid = random.choice(raids.raid)
      await RiZoeL.send_message(user, raid)
      await asyncio.sleep(0.3) 

async def start_dm_spam(RiZoeL, counts, user_id, spam_text):
   if int(user_id) in Devs:
      await message.reply_text("User is Dev of SpamX:)")
      return 
   for _ in range(counts):
      await RiZoeL.send_message(user_id, str(spam_text))
      await asyncio.sleep(0.3) 

async def start_dspam(RiZoeL, message, counts, delay, spam_text):
   chat = message.chat
   if chat.id in res_grps:
      await message.reply_text("**Sorry!** I can't spam here.")
      return
   if re.search(res_devs.lower(), spam_text.lower()):
      await message.reply_text("**Error!**")
      return
   for _ in range(counts):
      await RiZoeL.send_message(chat.id, str(spam_text))
      await asyncio.sleep(delay)

async def start_pspam(RiZoeL, message, counts):
   chat = message.chat
   if chat.id in res_grps:
      await message.reply_text("**Sorry!** I can't spam here.")
      return
   for _ in range(counts):
      prn = random.choice(plinks)
      if ".jpg" in prn or ".png" in prn:
        await RiZoeL.send_photo(chat.id, prn)
        await asyncio.sleep(0.4)
      if ".mp4" in prn or ".MP4," in prn:
        await RiZoeL.send_video(chat.id, prn)
        await asyncio.sleep(0.4)

""" Global Functions"""
async def start_gban(RiZoeL, message, user, reason):
    try:    
       x = await message.reply_text("Gbanning...")
       common = await RiZoeL.get_common_chats(user.id)
       done = 0
       fuck = 0
       if not common:
          await dor(message, x, f"User {user.mention} got no common chats with the specified one.")
          return
       for cht in common:  
         try:
           await RiZoeL.ban_chat_member(cht.id, user.id)
           done += 1
         except:
           fuck += 1
       await dor(message, x, f"user {user.mention} added in GBAN list!")

    except Exception as a:
      await message.reply_text(str(a))
      pass

async def start_ungban(RiZoeL, message, user):      
    try:
       x = await message.reply_text("Gbanning...")
       common = await RiZoeL.get_common_chats(user.id)
       done = 0
       fuck = 0
       if not common:
         await dor(message, x, f"User {user.mention} got no common chats with the specified one.")
         return
       for cht in common:  
         try:
           await RiZoeL.unban_chat_member(cht.id, user.id)
           done += 1
         except:
           fuck += 1
       await dor(message, x, f"user {user.mention} added in UNGBAN list!")

    except Exception as a:
      await message.reply_text(str(a))
      pass


async def start_gpromote(RiZoeL, message, user):
   x = await message.reply_text("promoting globally...")
   common = await RiZoeL.get_common_chats(user.id)
   chat_len = len(common)
   if not common:
      await dor(message, x, f"User {user.mention} got no common chats with the specified one.")
      return
   for cht in common:  
      try:
         await RiZoeL.promote_chat_member(cht.id, user.id, 
              can_change_info=True,
              can_manage_video_chats=True,
              can_delete_messages=True,
              can_restrict_members=True,
              can_invite_users=True,
              can_pin_messages=True,
              )
         done += 1
      except:
         fuck += 1
   await dor(message, x, f"User Globally Promoted ✓ \n\n User: {user.mention} \n total common chats: `{chat_len}` \n Promoted in `{done}` chats \n Failed in `{fuck}` chats")

async def start_gdemote(RiZoeL, message, user):
   x = await message.reply_text("demoting globally...")
   common = await RiZoeL.get_common_chats(user.id)
   chat_len = len(common)
   if not common:
      await dor(message, x, f"User {user.mention} got no common chats with the specified one.")
      return
   for cht in common:  
      try:
         await RiZoeL.promote_chat_member(cht.id, user.id, 
              can_change_info=False,
              can_manage_video_chats=False,
              can_delete_messages=False,
              can_restrict_members=False,
              can_invite_users=False,
              can_pin_messages=False,
              )
         done += 1
      except:
         fuck += 1
   await dor(message, x, f"User Globally demoted ✓ \n\n User: {user.mention} \n total common chats: `{chat_len}` \n Promoted in `{done}` chats \n Failed in `{fuck}` chats")
   

async def start_banall(RiZoeL, message):
   chat = message.chat
   x = RiZoeL.send_message(chat.id, "Hey it's SpamX!")
   done = 0
   failed = 0
   async for u in RiZoeL.get_chat_members(chat.id):
      user = u.user
      try:
         await RiZoeL.ban_chat_member(chat.id, user.id)
         done += 1
      except Exception as err:
         print(f"pyRiZoeLX - [INFO]: {str(err)}")
         failed += 1
   await x.delete()
   await RiZoeL.send_message(chat.id, f"Members Banned ✓ \n\n Banned {done} users\n failed {failed}")

async def get_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time

def start_spamX(RiZoeLX, type):
    if type == "token":
      RiZoeLX.start()
      try:
         x = RiZoeLX.get_me()
         print(f"pyRiZoeLX - [INFO]: @{x.username} started ✓")
      except:
         print(f"pyRiZoeLX - [INFO]: Bot started ✓")
    else:
      RiZoeLX.start()
      try:
         RiZoeLX.join_chat("RiZoeLX")
         RiZoeLX.join_chat("DNHxHELL")
      except:
         pass
      try:
         x = RiZoeLX.get_me()
         print(f"pyRiZoeLX - [INFO]: @{x.first_name} started ✓")
      except:
         print(f"pyRiZoeLX - [INFO]: Client started ✓")

def check_logchannel(chat_id):
   if chat_id in res_grps:
      return True
   else:
      return False
