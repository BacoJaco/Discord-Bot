import os
import discord
from discord.ext import commands
from discord.ui import Button, View
import random
import requests
import asyncio
import youtube_dl
from constant import keep_alive
import urllib.parse, urllib.request, re

intents = discord.Intents.all()
#Help Menu
helpCommand = commands.DefaultHelpCommand(no_catergory='Commands')
#Bot Prefix
bot = commands.Bot(command_prefix='.j ', intents=intents)

@bot.event
async def on_connect():
  print("Your bot is online")


#Addition
@bot.command(brief = "Put two numbers after the command to add them")
async def add(ctx, numOne, numTwo):
  solu = int(numOne) + int(numTwo)
  await ctx.reply("The solution to " + str(numOne) + " + " + str(numTwo) + " is " + str(solu))


#Time Greeting
@bot.command(brief = "Put in a time, such as 8 am, to get a greeting based on it")
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


#Random Images
imageList = ["https://miro.medium.com/max/960/1*kv9wKHnCwVhXWSUp4Luw_g.jpeg", "https://lp-cms-production.imgix.net/news/2017/06/GettyImages-538072290.jpg?auto=format&q=40&w=870&dpr=1", "https://media.nbcdfw.com/2021/07/GettyImages-888695410.jpg?quality=85&strip=all&resize=850%2C478", "https://cdntdreditorials2.azureedge.net/cache/c/2/8/e/9/6/c28e96f74b0a4672849199f3dafc16c46625457c.jpg", "https://i2.wp.com/nationaleconomicseditorial.com/wp-content/uploads/41bf0c3e58099d42176b2d327e6740a2.jpg?resize=678%2C381&ssl=1", "https://globalnews.ca/wp-content/uploads/2017/06/rubber-duck-e1507834750438.jpg?quality=85&strip=all&w=650&h=379&crop=1", "https://www.flare.com/wp-content/uploads/2017/05/Giant-rubber-duck-for-Canada-150-inline.jpg"]

@bot.command(brief = "This will output a random image of an oversized 'rubber' duck")
async def randomImage(ctx):
  num = random.randint(0, 6)
  imageAddress = imageList[num]
  await ctx.reply(imageAddress)


#8-Ball
@bot.command(brief = "Ask a question to recieve a mystical answer")
async def eightBall(ctx, *, phrase: str):
  ansList = [": **It is certain.**", ": **It is decidedly so.**", ": **Without a doubt.**", ": **Yes definitely.**", ": **You may rely on it.**", ": **As I see it, yes.**", ": **Most likely.**", ": **Outlook good.**", ": **Yes.**", ": **Signs point to yes.**", ": **Reply hazy, try again.**", ": **Ask again later.**", ": **Better not tell you now.**", ": **Cannot predict now.**", ": **Concentrate and ask again.**", ": **Don't count on it.**", ": **My reply is no.**", ": **My sources say no.**", ": **Outlook not so good.**", ": **Very doubtful.**"]
  ball = random.randint(0, 19)
  await ctx.reply(phrase + ansList[ball])


#Rock, Paper, Scissors
@bot.command(brief = "Type either rock, paper, or scissors to play", aliases = ["rps", "Rps"])
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


#Trivia
@bot.command(brief = "Type either 'multiple' or 'boolean' for multiple choice or true/false trivia")
async def trivia(ctx, type):
  triviaKey = os.environ['triviaKey']
  url = "https://opentdb.com/api.php?amount=1&category=9&difficulty=medium&type=" + type + "&key=" + triviaKey
  req = requests.get(url)
  data = req.json()
  question = data["results"][0]["question"]
  answer = data["results"][0]["correct_answer"]
  inanswer = data["results"][0]["incorrect_answers"]
  if type == "boolean":
    await ctx.send(question + ":  " + "True or False?" + "Reply with the answer to answer.")
  elif type == "multiple":
    await ctx.send(question + ":  " + inanswer[0] + ", " + str(answer) + ", " + inanswer[1] + ", " + inanswer[2] + ". Reply with the answer to answer.")
  else:
    await ctx.send("Type either 'multiple' or 'boolean'")
  try:
    msg = await bot.wait_for("message")
  except asyncio.TimeoutError:
    return await ctx.channel.send("Sorry, you took too long.")
  if msg.content == answer:
    await ctx.channel.send("Hooray, that's correct!")
  else:
    await ctx.channel.send("Wrong")


#Number Facts
@bot.command(brief = "Get random facts about a specific number")
async def number(ctx, num):
  url = "http://numbersapi.com/" + str(num) + "?json"
  req = requests.get(url)
  data = req.json()
  fact = data["text"]
  await ctx.send(fact)
  

#Music Player
@bot.command(brief = "Put in a YouTube link to play any song of your choice")
async def play(ctx, *, url):
  #Connecting to user channel
  voiceState = ctx.author.voice
  if voiceState is None:
    return await ctx.send("Join a voice channel to use this command.")
  if ctx.voice_client is None:
    await ctx.author.voice.channel.connect()
  else:
    ctx.voice_client.stop()
  
  #Generate link
  if not ("youtube.com/watch?" in url or "https://youtu.be/" in url):
    query_string = urllib.parse.urlencode({
      'search_query': url
    })
    html_content = urllib.request.urlopen(
      'https://www.youtube.com/results?' + query_string
    )
    search_results = re.findall(r"watch\?v=(\S{11})",html_content.read().decode())
    url = 'https://www.youtube.com/watch?v=' + search_results[0]
    YDL_OPTIONS={'format':"bestaudio"}
    vc = ctx.voice_client
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download = False)
      video_title = info.get('title', None)
    url2 = info['formats'][0]['url']
    source = await discord.FFmpegOpusAudio.from_probe(url2)
  
  #Getting YouTube data 
  YDL_OPTIONS={'format':"bestaudio"}
  vc = ctx.voice_client
  with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
    info = ydl.extract_info(url, download = False)
    video_title = info.get('title', None)
  url2 = info['formats'][0]['url']
  source = await discord.FFmpegOpusAudio.from_probe(url2)

  #Pause/Resume Functions
  button1 = Button(label = "Pause ⏸️")
  async def pauseClicked(interaction):
    try:
      ctx.voice_client.pause()
      await interaction.response.send_message("**Paused**")
    except:
      await interaction.response.send_message("No music to pause")
  
  button2= Button(label = "Resume ▶️")
  async def playClicked(interaction):
    try:
      ctx.voice_client.resume()
      await interaction.response.send_message("**Resumed**")
    except:
      await interaction.response.send_message("No music to resume")
  button1.callback = pauseClicked
  button2.callback = playClicked
  view = View()
  view.add_item(button1)
  view.add_item(button2)
  await ctx.send("**Now Playing: **" + video_title + " **(Type '.j stop' to end playback)**", view=view)
  
  #Returning music data+buttons
  vc.play(source)

@bot.command(brief = "Disconnect the bot from a voice channel and stop music playback")
async def stop(ctx):
  await ctx.voice_client.disconnect()
  await ctx.send("**Disconnected**")
  

#Connect Bot
keep_alive()
token = os.environ['token']
bot.run(token)