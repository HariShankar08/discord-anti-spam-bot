from datetime import datetime
from threading import Timer

import discord

from config import TOKEN

client = discord.Client()

details = {}


def make_message_info(msg: discord.Message):
    return {
        'time': datetime.now(),
    }


def remove_first(id):
    try:
        details[id].pop(0)
    except IndexError:
        pass


def add_info(id: int, msg: discord.Message):
    if id not in details:
        details[id] = [make_message_info(msg)]
    else:
        details[id].append(make_message_info(msg))

    t = Timer(60, remove_first, [id])
    t.start()


@client.event
async def on_ready():
    print('Logged in!')


@client.event
async def on_message(msg: discord.Message):
    if msg.author == client.user:
        return
    user: discord.Member = msg.author

    # content based deletion

    # this is NOT an empty string; it contains a zero width non joiner
    if msg.content.count('‌') >= 2:
        await msg.delete()

    # remove messages containing lots of newlines
    if msg.content.replace(' ', '').count('\n\n\n\n') > 0:
        await msg.delete()

    # time based deletion
    if user.id in details:
        user_details = details[user.id]

        now = datetime.now()
        if len(user_details) < 2:
            add_info(user.id, msg)
        else:
            t1 = (now-user_details[-1]['time']).total_seconds()
            t2 = (
                user_details[-1]['time'] -
                user_details[-2]['time']
            ).total_seconds()

            add_info(user.id, msg)
            if t1 < 2 and t2 < 2:
                await msg.delete()
    else:
        add_info(user.id, msg)

client.run(TOKEN)
