""" RiZoeLX 2022 © pyRiZoeLX """

""" Get User with Reason! """
async def get_user_reason(RiZoeL, message):
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

    return user, reason


async def get_user(RiZoeL, message):
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

    return user
