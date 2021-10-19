import discord
import math
import json
import requests
from discord.ext import commands
import os

def calculator(num1, operator, num2):
    if operator == "+":
        return num1 + num2
    elif operator == "-":
        return num1 - num2
    elif operator == "/":
        return num1 / num2
    elif operator == "x":
        return num1 * num2


def get_weather_data(city):
    apikey = os.environ['Weather']
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}"
    weather_response = requests.get(url).json()
    return weather_response

class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def calc(self, ctx, n1: float, op, n2: float):
        ans = calculator(n1, op, n2)
        await ctx.send(embed=discord.Embed(title='Calculator Result:', description=ans))
    

    @commmands.command()
    async def weather(self, ctx, *, city):
        em = discord.Embed(title="Weather", description = f"For {city}:")
        weather_response = get_weather_data(city)

        stime = weather_response['sys']['sunrise']
        sunrise = datetime.datetime.fromtimestamp(stime).strftime("%I:%M %p")
        em.add_field(name="Sunset:", value=f"Sunset is at {sunset}")

        stime = weather_response['sys']['sunset']
        sunset = datetime.datetime.fromtimestamp(stime).strftime("%I:%M %p")
        em.add_field(name="Sunrise:", value=f"Sunrise is at {sunrise}")

        min = weather_response['main']['temp_min']
        min = math.floor(min-273.15)
        max = weather_response['main']['temp_max']
        max = math.floor(max-273.15)
        em.add_field(name="Min/Max:", value=f"Minimum Temperature today is {min} And the max will be {max}")

        feelslike = weather_response['main']['feels_like']
        feelslike = math.floor(feelslike-273.15)
        em.add_field(name="Feels Like:", value=f"It feels like {feelslike} degrees celsius")

        temp = weather_response['main']['temp']
        temp = math.floor(temp-273.15)
        em.add_field(name="Temerature:",value=f"The temperature is {temp} degrees celsius")

        desc = weather_response['main'][0]["description"]
        main = weather_response['main'][0]['main']
        em.add_field(name="Description:", value=f"Weather description {main}, {desc}")

        await ctx.send(embed=em)



def setup(client):
    client.add_cog(Utilities(client))

apikey = "6f9aa23390668e72710bd5a33e3d575c"