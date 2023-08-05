""""
   © RiZoeLX
"""

import asyncio

async def dr(message, editor, text):
   try:
     await editor.edit_text(text)
   except:
     await editor.delete()
     await message.reply_text(text)

async def srape(RiZoeL, message, to_grp, from_grp):
   x = message.reply_text("processing...")
   try:
     await RiZoeL.join_chat(from_grp)
     try:
       scrape_group = await RiZoeL.get_chat(from_grp)
     except Exception as err:
       await dr(message, x, str(err))
       return
   except Exception as err:
     await dr(message, x, str(err))
     return
   print(f"[INFO]: joined {scrape_group.title} to scrape users")
   
   try:
     await RiZoeL.join_chat(to_grp)
     try:
       add_group = await RiZoeL.get_chat(to_grp)
     except Exception as err:
       await dr(message, x, str(err))
       return
   except Exception as err:
     await dr(message, x, str(err))
     return
   print(f"pyRiZoeLX [INFO]: joined {add_group.title} to add users")

   a = 0
   b = 0
   async for x in RiZoeL.get_chat_members(scrape_group.id):
        user = x.user
        try:
           await RiZoeL.add_chat_members(add_group, user.id)
           a += 1
           await asyncio.sleep(2)
        except Exception as a:
           b += 1
           print(f"[SpamX INFO]: {str(a)}")
   done_text = f"**Members Scraped ✓ \n\n Total {a} users added \n {b} users failed to add \n From chat: {scrape_group.title}"
   await dr(message, x, done_text)
