import discord
import os
import requests
import json
import random
from replit import db
from mainServer import runServer
import wikipedia

client = discord.Client()


# Calculator Functions
def sub(n1: float , n2: float):#Subtraction
  return n1 - n2

def add(n1: float, n2: float):#Addition
  return n1 + n2

def div(n1: float, n2: float):#Division
  return n1 / n2

def mul(n1:float, n2: float):#Multiplication
  return n1 * n2



# Motivator
sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'depressing']

starter_encouragements = [
  'Cheer up!',
  'Hang in there!',
  'You are a great person'
]

if "responding" not in db.keys():
  db["responding"] = True


# Miscellaneous
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote


def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]
    db["encouragements"].append(starter_encouragements)


def delete_encouraging_message(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements


def get_joke():
  link = "https://official-joke-api.appspot.com/random_joke"
  data = requests.get(link)
  joke =json.loads(data.text)
  return joke


def wiki_summary(arg):
  definition = wikipedia.summary(arg, sentences=3, chars=1000,
  auto_suggest=True, redirect=True
  )
  return definition


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('Hi'):
    await message.channel.send('Hi!\nNice to meet you')

  if message.content.startswith('hi'):
    await message.channel.send('Hi!\nNice to meet you')

  if message.content.startswith('Hello'):
    await message.channel.send('Hi!\nNice to meet you')

  if message.content.startswith('hello'):
    await message.channel.send('Hi!\nNice to meet you')

  if message.content.startswith('thought'):
    quote = get_quote()
    await message.channel.send(quote)
  
  if message.content.startswith('joke'):
    joke = get_joke()
    await message.channel.send(joke['type'])
    await message.channel.send(joke['setup'])
    await message.channel.send(joke['punchline'])

  msg = message.content
  options = starter_encouragements


  if db["responding"]:
    if "encouragements" in db.keys():
      options.extend(db["encouragements"])

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))


  # Help Message
  help_message = "Hi, my name is Neobot." + "\n" + "I am a bot which can do lot of stuff for you like" + "\n" + "1. I can search for thought for the day: Use keyword thought, Crack Some jokes with you etc.: Use keyword joke" + "\n" + "Act as a calculator, for that use the following commands:" + "\n" + "Addition: $add 2 + 4(u can use any number in place of 4 and 2 just type the command properly)" + "\n" + "Subtraction: $subtract 4 - 2" + "\n" + "Division: $divide 4 / 2" + "\n" + "Multiplication: $multiply 4 * 2" + "\n" + "I am still under development. Also I am case sensitive so type the commands properly" + "\n" + "\n" + "Owner: Shourya Sharma"


  if message.content.startswith('help') or message.content.startswith('Help'):
    await message.channel.send(help_message)

  if message.content.startswith("$new"):
    encouraging_message = msg.split("$new ", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added")


  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del", 1)[1])
      delete_encouraging_message(index)
      encouragements = db["encouragements"]
      await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ", 1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Now, the bot will respond to sad messages")
    
    else:
      db["responding"] = False
      await message.channel.send("Now, the bot will not respond to sad messages")

  if message.content.startswith("$add"):
    n1 = int(msg.split()[1])
    n2 = int(msg.split()[3])
    sum = discord.Embed(title="Sum", description=add(n1, n2), colour=discord.Colour.purple())
    await message.channel.send(content=None, embed=sum)

  if message.content.startswith("$subtract"):
    n1 = int(msg.split()[1])
    n2 = int(msg.split()[3])
    difference = discord.Embed(title="Difference", description=sub(n1, n2), colour=discord.Colour.purple())
    await message.channel.send(content=None, embed=difference)

  if message.content.startswith("$divide"):
    n1 = int(msg.split()[1])
    n2 = int(msg.split()[3])
    quotient = discord.Embed(title="Quotient", description=div(n1, n2), colour=discord.Colour.purple())
    await message.channel.send(content=None, embed=quotient)

  if message.content.startswith("$multiply"):
    n1 = int(msg.split()[1])
    n2 = int(msg.split()[3])
    product = discord.Embed(title="Product", description=mul(n1, n2), colour=discord.Colour.purple())
    await message.channel.send(content=None, embed=product)

  words = message.content.split()
  important_words = words[1:]

  if message.content.startswith("$define"):
    words = message.content.split()
    important_words = words[1:]
    search=discord.Embed(title="Searching...", description=wiki_summary(important_words), colour=discord.Colour.purple())
    await message.channel.send(content=None, embed=search)
  

# Starting the Web Server
runServer()

client.run(os.environ['TOKEN'])
