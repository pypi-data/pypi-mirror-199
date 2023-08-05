

# [Telethon || Red7 scanner]
from telethon.tl import types, functions
from PhoenixScanner import Phoenix

RIGHTS = types.ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

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

async def Red7_Watch_telethon(RiZoeL, message):
   if message.user_joined or message.added_by:
     user = message.sender_id
     Red7_Client = Phoenix(random_token())
     msg = f"""
 Alert ⚠️
User [{user}](tg://user?id={user}) is officially
Scanned by Team Red7 | Phoenix API ;)
Appeal [Here](https://t.me/Red7WatchSupport)
     """
     try:
        try:
           check = Red7_Client.check(user)
           if check['is_gban']:
              try:
                 await RiZoeL(functions.channels.EditBannedRequest(message.chat_id, user, BANNED_RIGHTS))
                 await RiZoeL.send_message(message.chat_id, msg, link_preview=False)
              except BaseException:
                pass
        except Exception:
           SCANLIST = []
           SCANLIST = update_scanlist(Red7_Client)
           if user in SCANLIST:
              try:
                 await RiZoeL(functions.channels.EditBannedRequest(message.chat_id, user, BANNED_RIGHTS))
                 await RiZoeL.send_message(message.chat_id, msg, link_preview=False)
              except BaseException:
                 pass
     except Exception as error:
        print(str(error))
