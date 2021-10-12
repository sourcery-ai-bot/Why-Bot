import discord
import random
from discord.ext import commands
from roastlist import roastlistpy

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rps(self, ctx, rps:str):
        choices = ["rock", "paper", "scissors"]
        cpu_choice = random.choice(choices)
        em = discord.Embed(title="Rock Paper Scissors")
        rps = rps.lower()
        if rps == 'rock':
            if cpu_choice == 'rock':
                em.description = "It's a tie!"
            elif cpu_choice == 'scissors':
                em.description = "You win!"
            elif cpu_choice == 'paper':
                em.description = "You lose!"

        elif rps == 'paper':
            if cpu_choice == 'paper':
                em.description = "It's a tie!"
            elif cpu_choice == 'rock':
                em.description = "You win!"
            elif cpu_choice == 'scissors':
                em.description = "You lose!"

        elif rps == 'scissors':
            if cpu_choice == 'scissors':
                em.description = "It's a tie!"
            elif cpu_choice == 'paper':
                em.description = "You win!"
            elif cpu_choice == 'rock':
                em.description = "You lose!"

        else:
            em.description = "Invalid Input"

        em.add_field(name="Your Choice", value=rps)
        em.add_field(name="Bot Choice", value=cpu_choice)
        await ctx.send(embed=em)


    @commands.command()
    async def roast(ctx):
        roast = random.choice(roastlistpy)
        em = discord.Embed(title=roast)
        await ctx.send(embed=em)


    @commands.command()
    async def dm(ctx, member: discord.Member, *, message):
        await ctx.channel.purge(limit=1)
        embeddm = discord.Embed(title=message)
        await member.send(embed=embeddm)


    @commands.command()
    async def sendroast(ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)
        message = random.choice(roastlistpy)
        embeddm = discord.Embed(
            title=message, description="Imagine being roasted by a bot")
        await member.send(embed=embeddm)

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        _8ballans = [
            "As I see it, yes",
            "It is certain",
            "It is decidedly so",
            "Most likely",
            "Outlook good",
            "Signs point to yes",
            "Without a doubt",
            "Yes",
            "Yes - definitely",
            "You may rely on it",
            "Reply hazy, try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful"
        ]
        em = discord.Embed(title="__8 Ball__",
                        description=f"{question}\nAnswer: {random.choice(_8ballans)}")
        await ctx.send(embed=em)


    @commands.command()
    async def embed(self, ctx, fields:str, extra:int, img:str=None):
        def wfcheck(m):
            return m.channel == ctx.channel and m.author == ctx.author
        em = discord.Embed()
        if fields == "t":
            await ctx.send("Enter Title:", delete_after=5)
            title = await self.client.wait_for("message", check=wfcheck)
            em.title = title.content
        if fields == "d":
            await ctx.send("Enter Description:", delete_after=5)
            desc = await self.client.wait_for("message", check=wfcheck)
            em.description = desc.content
        if fields == "td":
            await ctx.send("Enter Title:", delete_after=5)
            title = await self.client.wait_for("message", check=wfcheck)
            em.title = title.content

            await ctx.send("Enter Description:", delete_after=5)
            desc = await self.client.wait_for("message", check=wfcheck)
            em.description = desc.content

        if extra == 0:
            pass

        else:
            for i in range(extra):
                await ctx.send("Enter Name:", delete_after=5)
                name = await self.client.wait_for("message", check=wfcheck)

                await ctx.send("Enter Value:", delete_after=5)
                value = await self.client.wait_for("message", check=wfcheck)
                
                em.add_field(name=name.content, value=value.content)
        
        if img == None:
            pass
        else:
            em.set_image(url=img)

        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Fun(client))

