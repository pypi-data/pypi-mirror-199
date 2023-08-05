import time

async def extract_time(message, time_):
    if any(time_.endswith(unit) for unit in ("m", "h", "d")):
        unit = time_[-1]
        time_num = time_[:-1]  #type: str
        if not time_num.isdigit():
           await message.reply("Invalid time amount specified.")
           return ""
        if unit == "m":
            xtime = int(time_num) * 60
        elif unit == "h":
            xtime = int(time_num) * 60 * 60
        elif unit == "d":
            xtime = int(time_num) * 24 * 60 * 60
        else:
            return
        return xtime
    else:
        await message.reply(f"Invalid time type specified. Expected m,h, or d, got: {time_[-1]})
        return False


def get_time(time: int):
    if time >= 86400:
        time = int(time / (60 * 60 * 24))
        unit = "days"
    elif time >= 3600 < 86400:
        time = int(time / (60 * 60))
        unit = "hours"
    elif time >= 60 < 3600:
        time = int(time / 60)
        unit = "minutes"
    return " {} {}".format(time, unit)
