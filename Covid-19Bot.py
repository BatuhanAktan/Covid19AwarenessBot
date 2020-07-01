import discord
from discord.ext import commands, tasks
from newsapi import NewsApiClient
from itertools import cycle

newsap = NewsApiClient(api_key='507b6234e84e407e8a58a30af4e9ca1c')
client = commands.Bot(command_prefix='!')
status = cycle(["!help", "Spreading Awareness"])
client.remove_command('help')


@client.event
async def on_ready():
    change_status.start()
    print('Bot is Ready')


@client.command()
async def symptoms(ctx):
    await ctx.send('https://www.toronto.ca/wp-content/uploads/2020/04/8cd7-Symptoms-of-Covid-19-Banner.png')


@client.command()
async def news(ctx):
    firstArticle = str(newsap.get_top_headlines(q="covid 19")['articles'][0]['url'])
    await ctx.send(firstArticle)


@client.command()
async def help(message):
    await message.channel.send("Prefix ! \nsymptoms     Common Symptoms of COVID-19" +
                               "\nnews         Most recent news about COVID-19")


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


client.run('NzI3OTQwMzU0OTAwNDkyMzU4.XvzJVQ.zx-HNS68Rao80a8Er4f20mo5e18')
