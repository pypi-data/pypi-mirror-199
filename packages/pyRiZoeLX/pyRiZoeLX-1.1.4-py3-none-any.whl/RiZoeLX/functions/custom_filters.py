""" RiZoeLX 2022 © pyRiZoeLX """

from pyrogram import filters

def sudo_filter(Sudos, cmd: str):
   return filters.user(Sudos) & filters.command(cmd)

def me_filter(cmd: str):
   return filters.me & filters.command(cmd)

def private_filter(cmd, str):
   return filters.private & filters.incoming & filters.command(cmd)

def group_filter(cmd, str):
   return filters.group & filters.command(cmd)

def media_filter():
   return filters.photo & filters.video & filters.document & filters.audio & filters.voice
