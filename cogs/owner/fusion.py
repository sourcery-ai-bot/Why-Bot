import discord
import json
from discord.ext import commands
import datetime
import dotenv
from utils import is_it_me, Log, kwarg_to_embed
import time

log = Log()

dotenv.load_dotenv()

class Fusion(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.check(is_it_me)
    async def serverlist(self, ctx):
        servers = list(self.client.guilds)
        await ctx.send(f"Connected on {str(len(servers))} servers:")
        await ctx.send('\n'.join(guild.name for guild in servers))


    @commands.command()
    @commands.check(is_it_me)
    async def svrls(self, ctx):
      await ctx.message.delete()
      for guild in self.client.guilds:
        em = discord.Embed(title=guild.name, color=ctx.author.color)
        em.timestamp = datetime.datetime.utcnow()
        em.add_field(name="ID:", value=guild.id)
        em.add_field(name="Owner name", value=guild.owner.name)
        em.add_field(name="Member Count", value=guild.member_count)
        await ctx.author.send(embed=em)
        
    
    @commands.command()
    @commands.check(is_it_me)
    async def message_servers(self, ctx, *, kwargs):
        data = await kwarg_to_embed(self.client, ctx, kwargs)
        em = data[0]

        data = await self.client.get_db()
        for guild in self.client.guilds:
            if data[str(guild.id)]["announcement_channel"] is None:
                try:
                    await guild.system_channel.send(embed=em)
                except Exception:
                    continue
            else:
                try:
                    channel = await self.client.fetch_channel(int(data[str(guild.id)]["announcement_channel"]))
                    await channel.send(embed=em)
                except Exception:
                    continue
    

    @commands.command()
    @commands.check(is_it_me)
    async def msgserver(self, ctx, id:int, *, message):
        for guild in self.client.guilds:
            if guild.id == id:
                return await guild.text_channels[0].send(message)
        await ctx.send("guild not found")


    @commands.command()
    @commands.check(is_it_me)
    async def logs(self, ctx):
      file = discord.File("./database/log.txt")
      await ctx.author.send(file=file)


    @commands.command()
    @commands.check(is_it_me)
    async def ssinfo(self, ctx, g:int):
        guild = self.client.get_guild(g)
        print(guild)
        em = discord.Embed(title="Server Info:", description=f"For: {guild.name}", color=ctx.author.color)
        em.set_thumbnail(url=guild.icon.url)
        em.set_author(name=f"Guild Owner: {guild.owner.name}", icon_url=guild.owner.avatar.url)
        em.add_field(name="Member Count:", value=guild.member_count) 
        em.add_field(name="Created: ", value=f"<t:{int(time.mktime(guild.created_at.timetuple()))}>")
        em.add_field(name="ID:", value=guild.id)
        await ctx.send(embed=em)


    @commands.command()
    @commands.check(is_it_me)
    async def needhelp(self, ctx):
        needhelp = []
        for i in self.client.commands:
            if i.help is None:
                needhelp.append(f"{i.name} | {i.cog_name}")
        await ctx.send("\n".join(needhelp))


    @commands.command()
    @commands.check(is_it_me)
    async def cmdtojson(self, ctx):
        commandlist = []
        for i in self.client.commands:
            print(i)
            if i.usage is None:
                pass
            else:
                if len(i.aliases) == 0:
                    aliases = None
                else:
                    aliases = i.aliases
                data = {
                    "name" : i.name,
                    "aliases" : aliases,
                    "description" : i.description,
                    "help" : i.help,
                    "category" : i.extras['category'].lower(),
                    "usage" : i.usage
                }
                commandlist.append(data)
        with open("./commands.json", 'w') as f:
            json.dump(commandlist, f, indent=4)
    

def setup(client):
    client.add_cog(Fusion(client))
