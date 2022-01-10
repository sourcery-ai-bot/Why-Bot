import discord
import discord
from discord.ext import commands
import json


async def get_counting_channel(guild):
    with open("./database/db.json") as f:
        data = json.load(f)
    for i in data:
        if i["guild_id"] == guild.id:
            return int(i["counting_channel"])
    return None

# Counting


async def counting(msg, guild, channel, m):
    try:
        msg = int(msg)
    except:
        return

    cc = await get_counting_channel(guild)

    if cc is None:
        return
    if channel.id == cc:
        with open("./database/counting.json") as f:
            data = json.load(f)
        with open('./database/db.json') as f:
            dataa = json.load(f)
        for i in dataa:
            if i['guild_id'] == guild.id:
                if i['lastcounter'] == None:
                    i['lastcounter'] = m.author.id
                    break
                elif i['lastcounter'] == m.author.id:
                    data[f"{guild.id}"] = 0
                    i['lastcounter'] = None
                    await m.add_reaction("❌")
                    em = discord.Embed(title=f"{m.author.name}, You ruined it!", description="Only one person at a time\nCount reset to zero")
                    with open("./database/counting.json", 'w') as f:
                        json.dump(data, f, indent=4)
                    with open("./database/db.json", 'w') as f:
                        json.dump(dataa, f, indent=4)
                    return await channel.send(embed=em)
                else:
                    i['lastcounter'] = m.author.id
                    break
                    
        if (data[f"{guild.id}"] + 1) == msg:
            data[f"{guild.id}"] += 1
            await m.add_reaction("✅")
        else:
            await m.add_reaction("❌")
            em = discord.Embed(title=f"{m.author.name}, You ruined it!", description=f"You were supposed to type `{(data[f'{guild.id}']+1)}`\nCount reset to zero")
            i['lastcounter'] = None
            data[f"{guild.id}"] = 0
            await channel.send(embed=em)
        with open("./database/counting.json", 'w') as f:
            json.dump(data, f, indent=4)
        with open("./database/db.json", 'w') as f:
            json.dump(dataa, f, indent=4)


class Counting(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):

        channel = message.channel
        msg = message.content
        guild = message.guild

        await counting(msg, guild, channel, message)


def setup(client):
    client.add_cog(Counting(client))