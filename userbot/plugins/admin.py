"""Get Administrators of any Chat*
Syntax: .get_admin"""
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantAdmin, ChannelParticipantCreator
from userbot.system import dev_cmd
from userbot import bot

@bot.on(dev_cmd("admin ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "**Admins in this Channel**: \n"
    should_mention_admins = False
    reply_message = None
    pattern_match_str = event.pattern_match.group(1)
    if "m" in pattern_match_str:
        should_mention_admins = True
        if event.reply_to_msg_id:
            reply_message = await event.get_reply_message()
    input_str = event.pattern_match.group(2)
    to_write_chat = await event.get_input_chat()
    chat = None
    if not input_str:
        chat = to_write_chat
    else:
        mentions_heading = "**Admins in {} questo gruppo: **\n".format(input_str)
        mentions = mentions_heading
        try:
            chat = await bot.get_entity(input_str)
        except Exception as e:
            await event.edit(str(e))
            return None
    try:
        async for x in bot.iter_participants(chat, filter=ChannelParticipantsAdmins):
            if not x.deleted:
                if isinstance(x.participant, ChannelParticipantCreator):
                    mentions += "\n 👑 [{}](tg://user?id={}) `{}`".format(x.first_name, x.id, x.id)
        mentions += "\n"
        async for x in bot.iter_participants(chat, filter=ChannelParticipantsAdmins):
            if not x.deleted:
                if isinstance(x.participant, ChannelParticipantAdmin):
                    mentions += "\n ⚜️ [{}](tg://user?id={}) `{}`".format(x.first_name, x.id, x.id)
            else:
                mentions += "\n `{}`".format(x.id)
    except Exception as e:
        mentions += " " + str(e) + "\n"
    if should_mention_admins:
        if reply_message:
            await reply_message.reply(mentions)
        else:
            await event.reply(mentions)
        await event.delete()
    else:
        await event.edit(mentions)
