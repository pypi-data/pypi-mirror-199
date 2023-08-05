from .admins import *
from .get_info import *
from .get_user import *
from .list import *
from .scraper import *
from .spamx import * 
from .purges import *
from .welcome_message import *
#from .voicechat import *
from .custom_filters import *
from .broadcast import *
from .watchers import *




""" Edit Or Reply Function """
async def delete_reply(message, editor, text):
   try:
     await editor.edit_text(text)
   except:
     await editor.delete()
     await message.reply_text(text)
