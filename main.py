import discord
import os
import requests
import json
from mainServer import runServer
import wikipedia
import pyjokes
from translate import Translator
import aiohttp
import random

client = discord.Client()


# Translator
def getTranslation(from_lang, to_lang, text):
    translator = Translator(to_lang=to_lang, from_lang=from_lang)
    translation = translator.translate(text)
    return translation


# Miscellaneous
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


def get_a_joke():
  joke = pyjokes.get_joke(language="en", category="all")
  return joke


def wiki_summary(arg):
    definition = wikipedia.summary(arg,
                                   sentences=3,
                                   chars=1000,
                                   auto_suggest=True,
                                   redirect=True)
    return definition


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    greeting1 = "Hi"
    greeting2 = "Hello"
    greet = "Hi, I am Winter, your personal companion"

    if message.content == greeting1 or message.content == greeting2:
        await message.channel.send(greet)

    elif message.content.startswith(
            greeting1.lower()) or message.content.startswith(
                greeting2.lower()):
        await message.channel.send(greet)

    if message.content.startswith('thought'):
        quote = get_quote()
        await message.channel.send(quote)

    msg = message.content

    # Help Message
    help_message = "Hi, my name is Winter." + "\n" + "I am a bot which can do lot of stuff for you like" + "\n" + "I can search for thought for the day: Use keyword thought, crack a joke use keyword $joke" + "\n" + "Share some tongue twisters use command $twister, Act as a calculator, for that use the following command:" + "\n" + "$calc: 4-3" + "\n" + "I can also make a quick wikipedia search for you, command: $search 'The word', I can also act as a translator, for example: $translate ,spanish,english,buenos dias" + "\n" + "I am case sensitive so type the commands properly, and copy the exact command" + "\n" + "\n" + "Developer: Shourya Sharma"

    myColour = discord.Colour.random()

    help_final = discord.Embed(title="About me",
                               description=help_message,
                               colour=myColour)

    if message.content.startswith('$help') or message.content.startswith(
            'Help'):
        await message.channel.send(content=None, embed=help_final)

    if message.content.startswith("$calc:"):
        msg = msg.split(':', 2)
        result = msg[1] + '=' + str(eval(msg[1]))
        final_result = discord.Embed(title="Result",
                                     description=result,
                                     colour=discord.Colour.random())
        await message.channel.send(content=None, embed=final_result)

    if message.content.startswith("$calc "):
        await message.channel.send("What about the colon idiot")

    if message.content.startswith("calc"):
        await message.channel.send(
            "what the hell dude, you can't even write a command properly, add a dollar before calc"
        )

    words = message.content.split()
    important_words = words[1:]

    if message.content.startswith("$search"):
        words = message.content.split()
        important_words = words[1:]
        search = discord.Embed(title="Searching...",
                               description=wiki_summary(important_words),
                               colour=discord.Colour.purple())
        await message.channel.send(content=None, embed=search)

    if message.content.startswith("$joke"):
        final_joke = get_a_joke()
        await message.channel.send(final_joke)

    if message.content.startswith("$twister"):
        final_twister = pyjokes.get_joke(language="de", category="twister")
        await message.channel.send(final_twister)

    if message.content.startswith("$translate"):
        msg = msg.split(',', 4)
        final_translated = getTranslation(to_lang=msg[2],
                                          from_lang=msg[1],
                                          text=msg[3])
        await message.channel.send(final_translated)

    memeEmbed = discord.Embed(title='', description='')
    if message.content.startswith("$meme"):
      async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            memeEmbed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await message.channel.send(embed=memeEmbed)
          




# Starting the Web Server
runServer()

client.run(os.environ['TOKEN'])
