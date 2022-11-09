import os
import discord
from discord.ext import commands
import random
import requests
import json
import asyncio

intents = discord.Intents.all()

helpCommand = commands.DefaultHelpCommand(no_catergory='Commands')

bot = commands.Bot(command_prefix='.j ', intents=intents)

imageList = ["https://miro.medium.com/max/960/1*kv9wKHnCwVhXWSUp4Luw_g.jpeg", "https://lp-cms-production.imgix.net/news/2017/06/GettyImages-538072290.jpg?auto=format&q=40&w=870&dpr=1", "https://media.nbcdfw.com/2021/07/GettyImages-888695410.jpg?quality=85&strip=all&resize=850%2C478", "https://cdntdreditorials2.azureedge.net/cache/c/2/8/e/9/6/c28e96f74b0a4672849199f3dafc16c46625457c.jpg", "https://i2.wp.com/nationaleconomicseditorial.com/wp-content/uploads/41bf0c3e58099d42176b2d327e6740a2.jpg?resize=678%2C381&ssl=1", "https://globalnews.ca/wp-content/uploads/2017/06/rubber-duck-e1507834750438.jpg?quality=85&strip=all&w=650&h=379&crop=1", "https://www.flare.com/wp-content/uploads/2017/05/Giant-rubber-duck-for-Canada-150-inline.jpg"]

@bot.event
async def on_connect():
  print("Your bot is online")



@bot.command()
async def hello(ctx):
  await ctx.reply("Hello!")

@bot.command()
async def name(ctx, name):
  await ctx.reply("Hello " + name + ", nice to meet you!")

@bot.command()
async def add(ctx, numOne, numTwo):
  solu = int(numOne) + int(numTwo)
  await ctx.reply("The solution to " + str(numOne) + " + " + str(numTwo) + " is " + str(solu))

@bot.command()
async def time(ctx, time, period):
  if period.lower() == "am" and int(time) >= 5:
    await ctx.reply("Good morning!")
  elif period.lower() == "am" and int(time) <= 4:
    await ctx.reply("Good night!")
  elif period.lower() == "pm" and int(time) <= 4:
    await ctx.reply("Good afternoon!")
  elif period.lower() == "pm" and int(time) >= 5 and int(time) <= 7:
    await ctx.reply("Good evening!")
  elif period.lower() == "pm" and int(time) >= 8:
    await ctx.reply("Good Night!")

   
@bot.command()
async def image(ctx):
  await ctx.reply("https://miro.medium.com/max/960/1*kv9wKHnCwVhXWSUp4Luw_g.jpeg")

@bot.command()
async def randomImage(ctx):
  num = random.randint(0, 6)
  imageAddress = imageList[num]
  await ctx.reply(imageAddress)

@bot.command()
async def eightBall(ctx, *, phrase: str):
  ansList = [": **It is certain.**", ": **It is decidedly so.**", ": **Without a doubt.**", ": **Yes definitely.**", ": **You may rely on it.**", ": **As I see it, yes.**", ": **Most likely.**", ": **Outlook good.**", ": **Yes.**", ": **Signs point to yes.**", ": **Reply hazy, try again.**", ": **Ask again later.**", ": **Better not tell you now.**", ": **Cannot predict now.**", ": **Concentrate and ask again.**", ": **Don't count on it.**", ": **My reply is no.**", ": **My sources say no.**", ": **Outlook not so good.**", ": **Very doubtful.**"]
  ball = random.randint(0, 19)
  await ctx.reply(phrase + ansList[ball])

@bot.command(aliases = ["rps", "Rps"])
async def RPS(ctx, choice):
  choiceList = ["rock", "paper", "scissors"]
  choice = choice.lower()
  bChoice = random.choice(choiceList)
  if bChoice == choice:
    await ctx.reply("You chose " + "**" + choice + "**" + ", I chose " + "**" + bChoice + "**" + ", it's a tie!")
  elif choice == choiceList[0] and bChoice == choiceList[2] or choice == choiceList[1] and bChoice == choiceList[0] or choice == choiceList[2] and bChoice == choiceList[1]:
    await ctx.reply("You chose " + "**" + choice + "**" + ", I chose " + "**" + bChoice + "**" + ", you win!")
  elif choice == choiceList[0] and bChoice == choiceList[1] or choice == choiceList[1] and bChoice == choiceList[2] or choice == choiceList[2] and bChoice == choiceList[0]:
    await ctx.reply("You chose " + "**" + choice + "**" + ", I chose " + "**" + bChoice + "**" + ", you lose!")
  else:
    await ctx.reply("Type either rock, paper, or scissors. It's in the name.")

#@bot.command()
#async def joke(ctx):
#  url = "https://official-joke-api.appspot.com/random_joke"
#  req = requests.get(url)
#  data = req.json()
#  setup = data["setup"]
#  punchline = data["punchline"]
#  await ctx.send(setup)
#  await asyncio.sleep(3)
#  await ctx.send(punchline)

#@bot.command()
#async def weather(ctx, zip):
#  my_weather = os.environ['weatherKey']
#  url = "https://api.openweathermap.org/data/2.5/weather?zip=" + zip + #",US&appid=" + my_weather
#  req = requests.get(url)
#  data = req.json()
#  weather = data["weather"][0]["description"]
#  temp = data["main"]["temp"]
#  temp = (temp - 273.5) * 9/5 + 32
#  #round temp
#  temp = round(temp, 1)
#  await ctx.send(weather + ", " + str(temp) + " degrees F")


@bot.command()
async def trivia(ctx, type):
  url = "https://opentdb.com/api.php?amount=1&category=9&difficulty=medium&type=" + type
  req = requests.get(url)
  data = req.json()
  question = data["results"][0]["question"]
  answer = data["results"][0]["correct_answer"]
  inanswer = data["results"][0]["incorrect_answers"]
  await ctx.send(question + ":  " + inanswer[0] + ", " + str(answer) + ", " + inanswer[1] + ", " + inanswer[2] + ". Reply with the answer to answer.")
  try:
    msg = await bot.wait_for("message")
  except asyncio.TimeoutError:
    return await ctx.channel.send("Sorry, you took too long.")
  
  if msg.content == answer:
    await ctx.channel.send("Hooray, that's correct!")
  else:
    await ctx.channel.send("Wrong")

  
#@bot.command()
#async def answer(ctx, sol):
    #if sol.lower() == answer.lower():
    #  await ctx.send("Hooray")
    #else:
    #  await ctx.send("Wrong")

@bot.command()
async def number(ctx, num):
  url = "http://numbersapi.com/" + str(num) + "?json"
  req = requests.get(url)
  data = req.json()
  fact = data["text"]
  await ctx.send(fact)




token = os.environ['token']
bot.run(token)

