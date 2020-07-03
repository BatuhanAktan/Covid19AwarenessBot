import discord
from discord.ext import commands, tasks
from newsapi import NewsApiClient
from itertools import cycle
import covid19_data
import requests

apiKey = ""
SearchEngineId = "016022283749187198618:hzvadnmjhwa"
newsap = NewsApiClient(api_key='')
client = commands.Bot(command_prefix='!')
status = cycle(["!help", "Spreading Awareness"])
client.remove_command('help')
loca = "number of cases in Mississauga july 2"
page = 1


@client.event
async def on_ready():
    change_status.start()
    print('Bot is Ready')


@client.command()
async def symptoms(ctx):
    await ctx.send('https://www.toronto.ca/wp-content/uploads/2020/04/8cd7-Symptoms-of-Covid-19-Banner.png')


@client.command()
async def news(ctx):
    firstarticle = str(newsap.get_top_headlines(q="covid 19")['articles'][0]['url'])
    await ctx.send(firstarticle)


@client.command()
async def help(message):
    await message.channel.send("```Prefix                     !                   " +
                               "\n\nCommands\n                                      "
                               "\nsymptoms     Common Symptoms of COVID-19\n" +
                               "\nnews         Most recent news about COVID-19\n" +
                               "\nlocation **City/Country**   Most visited sources for a specific region\n"+
                               "\ncases **Country**       Number of confirmed cases\n"+
                               "\ndeaths **Country**      Number of confirmed deaths\n"+
                               "\nrecoveries **Country**  Number of confirmed recoveries```\n")


@client.command()
async def location(message, *, loca):
    covidLoca = "covid 19" + loca
    url = f"https://www.googleapis.com/customsearch/v1?key={apiKey}&cx={SearchEngineId}&q={covidLoca}&start={(page - 1) * 10 + 1}"
    data = requests.get(url).json()
    search_items = data.get("items")
    for i, search_item in enumerate(search_items, start=1):
        link = search_item.get("link")
    print(link)
    await message.channel.send(link)


@location.error
async def missing(message, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await message.send("Please Specify a Location")
    else:
        await message.send("Something Went Wrong")


@client.command()
async def cases(message, *,country):
    case = covid19_data.dataByName(str(country))
    print(case.cases)
    mes = str(case.cases)+ " confirmed cases in " + str(country)
    await message.channel.send(mes)


@cases.error
async def eror(message, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await message.send("Please Specify a Location")
    else:
        await message.send("Something Went Wrong")


@client.command()
async def deaths(message, *,country):
    death = covid19_data.dataByName(str(country))
    print(death.deaths)
    mes = str(death.deaths) + " Deaths in " + str(country)
    await message.send(mes)


@deaths.error
async def eror(message, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await message.send("Please Specify a Location")
    else:
        await message.send("Something Went Wrong")


@client.command()
async def recoveries(message, *,country):
    recovery = covid19_data.dataByName(str(country))
    print(recovery.recovered)
    mes = str(recovery.recovered) + " recoveries in " + str(country)
    await message.send(mes)


@recoveries.error
async def eror(message, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await message.send("Please Specify a Location")
    else:
        await message.send("Something Went Wrong")


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


client.run('')
