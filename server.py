import markov
import discord
import os

# Run a webserver on a separate thread for heroku
# import threading
# from os import environ
# from flask import Flask

# app = Flask(__name__)
# worker = getattr(app, 'run')
# t = threading.Thread(target=worker, args=[environ.get('PORT')])
# t.start()

client = discord.Client()
markov = markov.Markov()

@client.event
async def on_ready():
    markov.init()
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # print(message)
    if message.author == client.user:
        return

    if message.content.lower().startswith("$tellme"):
        starting = message.content.split()[1].lower()
        num = int(message.content.split()[2])
        out = " ".join(markov.generate(starting, num))
        await message.channel.send(out)
    
    if message.content.lower().startswith('hows it going bot alan'):
        await message.channel.send(" ".join(markov.generate("i'm", 50)))

    if message.content.startswith('give me a sentence bot alan'):
        await message.channel.send(" ".join(markov.generate("the", 50)))

    # if message.content.startswith('$hello'):
    #     await message.channel.send('Hello!')

client.run(os.getenv("ALAN_TEXT_TOKEN"))

print("hi")