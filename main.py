import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import Paginator, Page, PaginatorButton
from list_of_cities import cities_chunked, cities_links, cities
from key import api_key

def str_chunk(chunk):
    return_string = ""
    for n in range(len(chunk) - 1):
        return_string = return_string + "(" + str(chunk[n]) + ")" + ", "
    return_string += "(" + str(chunk[len(chunk) - 1]) + ")" 
    return return_string

def find_listings(wanted_item, titles, li_elements):
    return_array = []
    n = 0
    for title in titles:
        if wanted_item in title.get_text().lower():
            return_array.append(li_elements[n].find('a').get('href'))  
        n+=1
    return return_array

intents = discord.Intents.default()
intents.message_content = True

r = requests.get('https://minneapolis.craigslist.org/search/sss?query=nintendo%20switch#search=1~gallery~0~0')
soup = BeautifulSoup(r.content, 'html.parser')
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = await client.fetch_channel(1129211497231417437)
    await channel.send("I'm here")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.startswith("$hello"):
            await message.channel.send('Hello ' + str(message.author))
    elif message.content.startswith("$list_cities"):
            await message.channel.send("Possible cities:")
            for n in range(11):
                await message.channel.send(str_chunk(cities_chunked[n]))
    elif message.content.startswith("$help"):
        await message.channel.send("""Possible commands:\n$hello - Say hello to me\n$list_cities - Lists the cities that can be searched in\n$find" city+item" - Finds all listings for the specified item in the specified city""")
    elif message.content.startswith("$find"):
        city_and_item = message.content[6:len(message.content)].split("+")

        link = cities_links[cities.index(city_and_item[0])] + "/search/sss?query="
        item = city_and_item[1].split(" ")
        for n in range(len(item)):
            link += item[n] + "%20"

        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'html.parser')
        li_elements = soup.find_all('li', class_='cl-static-search-result')
        titles = soup.find_all('div', class_='title')
        correct_listings = find_listings(city_and_item[1], titles, li_elements)
        Pages = []
        for n in range(len(correct_listings)):
            Pages.append(Page(content=n+1+"/"+len(correct_listings)), embeds = [correct_listings[n]])

@client.command()
async def

client.run(api_key)





