"""
   RiZoeLX 2022-2023 © pyRiZoeLX 
"""

from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped

async def play_audio(RiZoeL, message, pytg, audio, chat):
   try:
      await RiZoeL.join_chat(chat)
   except Exception as err:
      await message.reply_text(str(err))
      return
   await pytg.join_group_call(chat, AudioPiped(audio), stream_type=StreamType().pulse_stream)
