from datetime import datetime
from threading import Timer
import requests
import random
import discord
import asyncio

client = discord.Client()
webhook = None

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

random_words = requests.get('https://random-word-api.herokuapp.com/all').json()


@client.event
async def on_ready():
    print('Logged in!')


@client.event
async def on_message(msg: discord.Message):
    global webhook
    if msg.author == client.user:
        return
    user: discord.Member = msg.author

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
                if msg.author.display_name != 'urlocalwordspammer':
                    await msg.delete()
                
    else:
        add_info(user.id, msg)
        
    if '|make' in msg.content.lower():
        channel = msg.channel
        if webhook is None:
            webhook = await channel.create_webhook(name='Bot Need This Thanks')
        await msg.author.send('Ready to spam.')
        
    elif msg.content == '|start':
            while True:
                try:
                    await webhook.send(username="urlocalwordspammer", content=f"@everyone {random.choice(random_words)}")
                    await asyncio.sleep(1)
                except Exception as e:
                    await msg.author.send('Oh No. Something went wrong.')
                    await msg.author.send(str(e))
                    break
        
if __name__ == '__main__':
    client.run('ODI3Mzk3OTc2MDc0NDg1Nzgw.YGacaQ.h5MapmWuPuETUnVXQsCgHE3BtGo')
