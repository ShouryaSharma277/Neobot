# **Imports**
import discord
import os
import requests
import json
from Server import runServer
import wikipedia
import pyjokes
from translate import Translator
import aiohttp
import random

client = discord.Client()

# **Methods**
def translateHandler(from_lang, to_lang, text):
    translator = Translator(to_lang=to_lang, from_lang=from_lang)
    translation = translator.translate(text)
    return translation


def quoteHandler():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


def jokeHandler():
    joke = pyjokes.get_joke(language="en", category="all")
    return joke


def searchHandler(arg):
    definition = wikipedia.summary(arg,
                                   sentences=3,
                                   chars=1000,
                                   auto_suggest=True,
                                   redirect=True)
    return definition


# **Variables**
myColour = discord.Colour.random()
greeting1 = "Hi bot"
greeting2 = "hi bot"
greet = "Hi, I am Winter, your personal companion"
prefix = "."
help_message = "Hi, my name is Winter." + "\n" + "I am a bot which can do lot of stuff for you like" + "\n" + f"I can search for quote: Use keyword {prefix}quote, crack a joke use keyword {prefix}joke" + "\n" + f"Share some tongue twisters use command {prefix}twister, Act as a calculator, for that use the following command:" + "\n" + f"{prefix}calc: 4-3" + "\n" + f"I can also make a quick wikipedia search for you, command: {prefix}search 'The word', I can also act as a translator, for example: {prefix}translate ,spanish,english,buenos dias" + "\n" + "I am case sensitive so type the commands properly, and copy the exact command" + "\n" + f"Memes: {prefix}meme" + "\n" + "Developer: @⌬ ⟆ᖺᗝυᖇႸᎯ277 ⌬#2894"

# **Embeds**
help_final = discord.Embed(title="About me",
                           description=help_message,
                           colour=myColour)
memeEmbed = discord.Embed(title='', description='', colour=myColour)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # Some more variables inside the event
    msg = message.content
    words = message.content.split()
    important_words = words[1:]

    # Messaging
    if message.author == client.user:
        return

    if message.content == greeting1 or message.content == greeting2:
        await message.reply(greet)

    if message.content.startswith(f'{prefix}quote'):
        quote = quoteHandler()
        await message.reply(quote)

    if message.content == f"{prefix}help" or message.content == "help":
        await message.reply(content=None, embed=help_final)

    if message.content.startswith(f"{prefix}calc:"):
        msg = msg.split(':', 2)
        result = msg[1] + '=' + str(eval(msg[1]))
        final_result = discord.Embed(title="Result",
                                     description=result,
                                     colour=myColour)
        await message.reply(content=None, embed=final_result)

    if message.content.startswith(f"{prefix}calc "):
        await message.reply("What about the colon idiot")

    if message.content.startswith("calc"):
        await message.reply(
            f"what the hell dude, you can't even write a command properly, add a {prefix} before calc"
        )

    if message.content.startswith(f"{prefix}search"):
        words = message.content.split()
        important_words = words[1:]
        search = discord.Embed(title="Searching...",
                               description=searchHandler(important_words),
                               colour=myColour)
        await message.reply(content=None, embed=search)

    if message.content.startswith(f"{prefix}joke"):
        final_joke = jokeHandler()
        await message.reply(final_joke)

    if message.content.startswith(f"{prefix}twister"):
        final_twister = pyjokes.get_joke(language="de", category="twister")
        await message.reply(final_twister)

    if message.content.startswith(f"{prefix}translate"):
        msg = msg.split(',', 4)
        final_translated = translateHandler(to_lang=msg[2],
                                            from_lang=msg[1],
                                            text=msg[3])
        await message.reply(final_translated)

    if message.content.startswith(f"{prefix}meme"):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                    'https://www.reddit.com/r/dankmemes/new.json?sort=hot'
            ) as r:
                res = await r.json()
                memeEmbed.set_image(url=res['data']['children'][random.randint(
                    0, 25)]['data']['url'])

        await message.reply(embed=memeEmbed)
    

    # Setting the bot online/offline or any another possible thingy
    if message.content == f"{prefix}setDnd":
        await client.change_presence(status=discord.Status.dnd)

    elif message.content == f"{prefix}setOffline":
        await client.change_presence(status=discord.Status.invisible)
    
    elif message.content == f"{prefix}setIdle":
        await client.change_presence(status=discord.Status.idle)

    elif message.content == f"{prefix}setOnline":
        await client.change_presence(status=discord.Status.online)



# Starting the Web Server
runServer()
print("Alive at https://Winter.shouryasharma.repl.co")

client.run(os.environ['token'])
