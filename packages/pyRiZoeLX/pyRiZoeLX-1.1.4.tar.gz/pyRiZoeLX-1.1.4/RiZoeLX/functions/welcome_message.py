""" RiZoeLX 2022 © pyRiZoeLX """

import random 

async def custom_welcome(RiZoeL, message):
   chat = message.chat
   user = message.user
   welcome_text = random.choice(random_welcome)
   try:
      await RiZoeL.send_message(chat.id, welcome_text.format(user.mention))
   except:
      await RiZoeL.send_message(chat.id, welcome_text.format(user.mention, chat.title))

random_welcome = [
   'Heyy! {} Welcome to {}',
   'Hello {}! Nice to meet you, How are you?',
   '{} Joined the chat!',
   '{} New member here!',
   '{} Nice to meet you! Welcome to {}',
]
   
