"""
   RiZoeLX 2022 © pyRiZoeLX
"""

from PhoenixScanner import Phoenix
import random

def random_token():
   Toks = ["RED7-yppfpzmakyopbjiwyccs", 
           "RED7-s7gforbm7iga1bj34qvlsa",
           "RED7-riw5wtg5mpjlcxi6jtjqhh",
           "RED7-cwnwhnzu305f24304nrs38",
           "RED7-gsgqo3eoab0vqsx1fw808",
          ]
   token = random.choice(Toks)
   return token

def update_scanlist(Red7):
   newlist = Red7.scanlist()
   if newlist == {'message': 'Invalid Token'}:
      newlist = Red7.scanlist()
      if newlist == {'message': 'Invalid Token'}:
         raise 'Invalid Scanner Token'
   return newlist


# [Pyrogram]
async def Red7_Watch(RiZoeL, member):
   Red7_Client = Phoenix(random_token())
   if (
        member.new_chat_member
        and member.new_chat_member.status
        and not member.old_chat_member
   ):
        pass
   else:
        return
   
   user = member.new_chat_member.user if member.new_chat_member else member.from_user   
   msg = f"""
** Alert ⚠️**
User {user.mention} is officially
Scanned by Team Red7 | Phoenix API ;)
Appeal [Here](https://t.me/Red7WatchSupport)
   """
   try:
      try:
         check = Red7_Client.check(user.id)
         if check['is_gban']:
            try:
               await RiZoeL.ban_chat_member(member.chat.id, user.id)
               await RiZoeL.send_message(member.chat.id, msg, disable_web_page_preview=True)
            except Exception:
               return          
      except:
         SCANLIST = []
         SCANLIST = update_scanlist(Red7_Client)
         if user.id in SCANLIST:
            try:
               await RiZoeL.ban_chat_member(member.chat.id, user.id)
               await RiZoeL.send_message(member.chat.id, msg, disable_web_page_preview=True)
            except Exception:
               return           
   except Exception as error:
      print(str(error))

