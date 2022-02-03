import discord
from utils.checks import plugin_enabled
from discord.ext import commands
import random
from googleapiclient.discovery import build
from utils.other import log
import re
import urllib.request
import os
import praw
import dotenv
import requests

dotenv.load_dotenv()


isapi_key = "AIzaSyCj52wnSciil-4JPd6faOXXHfEb1pzrCuY"


def reddit_client():
    client = praw.Reddit(
        client_id=os.environ['CLIENT_ID'],
        client_secret=os.environ['CLIENT_SECRET'],
        user_agent="memes-fastapi"
    )
    return client


def is_image(post):
    try:
        return post.post_hint == "image"
    except AttributeError:
        return False


async def get_img_url(client: praw.Reddit, sub_name: str, limit: int):
    hot_memes = client.subreddit(sub_name).hot(limit=limit)
    image_urls = []
    for post in hot_memes:
        if is_image(post):
            image_urls.append(post.url)
    return image_urls


async def get_url(client: praw.Reddit, sub_name: str, limit: int):
    hot_memes = client.subreddit(sub_name).hot(limit=limit)
    urls = []
    for post in hot_memes:
        urls.append(post.url)
    return urls


class Search(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.animal_urls = {
            "dog" : "https://some-random-api.ml/animal/dog",
            "cat" : "https://some-random-api.ml/animal/cat",
            "fox" : "https://some-random-api.ml/animal/fox",
            "panda" : "https://some-random-api.ml/animal/panda",
            "bird" : "https://some-random-api.ml/animal/bird",
        }

    @commands.command(aliases=['is'], help="This command is used to search for images on google.", extras={"category":"Search"}, usage="imagesearch [search query]", description="Find an image from google")
    @commands.check(plugin_enabled)
    async def imagesearch(self, ctx, *, search):
        ran = random.randint(0, 9)
        resource = build("customsearch", "v1", developerKey=isapi_key).cse()
        result = resource.list(
            q=f"{search}", cx="54c1117c3e104029b", searchType="image"
        ).execute()
        url = result["items"][ran]["link"]
        embed1 = discord.Embed(title=f"Search:({search.title()})")
        embed1.set_image(url=url)
        await ctx.send(embed=embed1)

    @commands.command(aliases=['yt'], help="This command gets searches through youtube to find a video.", extras={"category":"Search"}, usage="youtube [search query]", description="Searches through youtube for videos")
    @commands.check(plugin_enabled)
    async def youtube(self, ctx, *, search_):
        search_ = search_.replace(" ", "+")
        html = urllib.request.urlopen(
            f'http://www.youtube.com/results?search_query={search_}')
        ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        base_url = "https://www.youtube.com/watch?v="
        em = discord.Embed(title="Youtube Search",
                           description="Showing first 5 urls")
        videos = [ids[0], ids[1], ids[2], ids[3], ids[4]]
        for video in videos:
            em.add_field(name=f"{base_url}{video}", value="** **")
        await ctx.send(embed=em)

    @commands.command(aliases=['rimg'], help="This command looks through a reddit subreddit of your choice and finds an image from that subreddit", extras={"category":"Search"}, usage="redditimg [subreddit]", description="Find a image from a subreddit")
    @commands.check(plugin_enabled)
    async def redditimg(self, ctx, subreddit: str):
        rclient = reddit_client()
        urls = await get_img_url(client=rclient, sub_name=subreddit, limit=50)
        url = random.choice(urls)
        em = discord.Embed(title="Reddit Image Search:")
        em.set_image(url=url)
        await ctx.send(embed=em)

    @commands.command(aliases=['getmeme'], help="This command looks in r/memes to find a meme", extras={"category":"Search"}, usage="meme", description="Gets a meme")
    @commands.check(plugin_enabled)
    async def meme(self, ctx):
        reddit = reddit_client()
        subreddit = reddit.subreddit("memes")
        hot = subreddit.hot(limit=50)
        urls = []
        for i in hot:
            urls.append(i)
        ran_sub = random.choice(urls)
        name = ran_sub.title
        url = ran_sub.url
        ups = ran_sub.ups
        downs = ran_sub.downs
        author = ran_sub.author
        em = discord.Embed(title=name)
        em.set_image(url=url)
        em.set_footer(text=f"{author} | 👍 : {ups}")
        await ctx.send(embed=em)

    @commands.command(aliases=['redditsearch'], help="This command looks though a reddit subreddit of your choice and finds a random post.", extras={"category":"Search"}, usage="reddit [subreddit]", description="Find a random reddit post")
    @commands.check(plugin_enabled)
    async def reddit(self, ctx, subreddit: str):
        rclient = reddit_client()
        urls = await get_url(client=rclient, sub_name=subreddit, limit=50)
        url = random.choice(urls)
        em = discord.Embed(title="Reddit Search:", description=url)
        await ctx.send(embed=em)
    
    @commands.command(help="This command returns a random rock image", extras={"category":"Search"}, usage="rock", description="Rock Image")
    @commands.check(plugin_enabled)
    async def rock(self, ctx):
        url = "https://mrconos.pythonanywhere.com/rock/random"
        while True:
            response = requests.get(url, headers={}, data={}).json()
            if response['image'] == "none":
                pass
            else:
                break
        em = discord.Embed(title=response['name'], description=response['desc'])
        rating = response["rating"]
        em.add_field(name="Rating", value=f"{rating}/5")
        em.set_image(url=response["image"])
        await ctx.send(embed=em)


    # Animals:
    @commands.command(help="This command show a picture of a dog", extras={"category":"Search"}, usage="dog", description="Dog Image")
    @commands.check(plugin_enabled)
    async def dog(self, ctx):
        url = self.animal_urls["dog"]
        r = requests.get(url).json()
        em = discord.Embed(title="Dog!", description=r['fact'])
        em.set_image(url=r['image'])

        await ctx.send(embed=em)
    
    @commands.command(help="This command show a picture of a cat", extras={"category":"Search"}, usage="cat", description="Cat Image")
    @commands.check(plugin_enabled)
    async def cat(self, ctx):
        url = self.animal_urls["cat"]
        r = requests.get(url).json()
        em = discord.Embed(title="Cat!", description=r['fact'])
        em.set_image(url=r['image'])

        await ctx.send(embed=em)

    @commands.command(help="This command show a picture of a panda", extras={"category":"Search"}, usage="panda", description="Panda Image")
    @commands.check(plugin_enabled)
    async def panda(self, ctx):
        url = self.animal_urls["panda"]
        r = requests.get(url).json()
        em = discord.Embed(title="Panda!", description=r['fact'])
        em.set_image(url=r['image'])

        await ctx.send(embed=em)

    @commands.command(help="This command show a picture of a fox", extras={"category":"Search"}, usage="fox", description="Fox Image")
    @commands.check(plugin_enabled)
    async def fox(self, ctx):
        url = self.animal_urls["fox"]
        r = requests.get(url).json()
        em = discord.Embed(title="Fox!", description=r['fact'])
        em.set_image(url=r['image'])

        await ctx.send(embed=em)

    @commands.command(help="This command show a picture of a bird", extras={"category":"Search"}, usage="bird", description="Bird Image")
    @commands.check(plugin_enabled)
    async def bird(self, ctx):
        url = self.animal_urls["bird"]
        r = requests.get(url).json()
        em = discord.Embed(title="Bird!", description=r['fact'])
        em.set_image(url=r['image'])

        await ctx.send(embed=em)

    
    @commands.command(help="This command shows a fake tweet image with the user you wants name on it and the message you want", extras={"category":"Search"}, usage="tweet [@person] [message]", description="Fake tweet image")
    @commands.check(plugin_enabled)
    async def tweet(self, ctx, member: discord.Member, *, message):
        data = {
            "username" : member.name,
            "displayname" : member.display_name,
            "avatar" : member.avatar.url,
            "comment" : message
        }

        url = "https://some-random-api.ml/canvas/tweet/"
        r = requests.get(url=url, data=data)
        with open(f"./tempstorage/tweet{ctx.author.id}.png", 'wb') as f:
            f.write(r.content)
        file = discord.File(f"./tempstorage/tweet{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/tweet{ctx.author.id}.png")

    @commands.command(aliases=['ytc'], help="This command shows a fake youtube comment image with the user you wants name on it and the message you want", extras={"category":"Search"}, usage="ytcomment [@person] [message]", description="Fake youtube comment image")
    @commands.check(plugin_enabled)
    async def ytcomment(self, ctx, member: discord.Member, *, message):
        data = {
            "username" : member.name,
            "avatar" : member.avatar.url,
            "comment" : message
        }

        url = "https://some-random-api.ml/canvas/youtube-comment/"
        r = requests.get(url=url, data=data)
        with open(f"./tempstorage/yt{ctx.author.id}.png", 'wb') as f:
            f.write(r.content)
        file = discord.File(f"./tempstorage/yt{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/yt{ctx.author.id}.png")

    @commands.command(help="This command shows a memeber profile pic on a simp card", extras={"category":"Search"}, usage="simp [@member]", description="Simp card")
    @commands.check(plugin_enabled)
    async def simp(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        data = {
            "avatar" : member.avatar.url,
        }

        url = "https://some-random-api.ml/canvas/simpcard/"
        r = requests.get(url=url, data=data)
        with open(f"./tempstorage/simp{ctx.author.id}.png", 'wb') as f:
            f.write(r.content)
        file = discord.File(f"./tempstorage/simp{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/simp{ctx.author.id}.png")

    @commands.command(help="This command shows your licence to be horny card", extras={"category":"Search"}, usage="horny [@member]", description="Horny licence")
    @commands.check(plugin_enabled)
    async def horny(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        data = {
            "avatar" : member.avatar.url,
        }

        url = "https://some-random-api.ml/canvas/horny/"
        r = requests.get(url=url, data=data)
        with open(f"./tempstorage/horny{ctx.author.id}.png", 'wb') as f:
            f.write(r.content)
        file = discord.File(f"./tempstorage/horny{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/horny{ctx.author.id}.png")

    @commands.command(help="This command is actually a bunch of commands. You type the command and then specify an overlay type, these are the options:\ngay, glass, wasted, passed, jail, comrade, triggered\nAfter you pick one the bot will put that as an overlay on top of the member you picked profile pictire", extras={"category":"Search"}, usage="overlay [type] [@member]", description="Image overlays for you discord profile pic")
    @commands.check(plugin_enabled)
    async def overlay(self, ctx, type:str=None, member: discord.Member=None):
        overlays = ["gay","glass","wasted","passed","jail","comrade","triggered"]
        if type is None or type.lower() not in overlays:
            return await ctx.send(embed=discord.Embed(title="Overlays:", description="\n".join(overlays)))

        if member is None:
            member = ctx.author
            
        data = {
            "avatar" : member.avatar.url,
        }

        url = f"https://some-random-api.ml/canvas/{type}/"

        r = requests.get(url=url, data=data)
        with open(f"./tempstorage/overlay{ctx.author.id}.png", 'wb') as f:
            f.write(r.content)
        file = discord.File(f"./tempstorage/overlay{ctx.author.id}.png")
        await ctx.send(file=file)
        os.remove(f"./tempstorage/overlay{ctx.author.id}.png")
    
    @commands.command(help="This command tells a (not funny) joke", extras={"category":"Search"}, usage="joke", description="Joke")
    @commands.check(plugin_enabled)
    async def joke(self, ctx):
        url = "https://some-random-api.ml/joke"
        r = requests.get(url).json()
        em=discord.Embed(title=r['joke'])

        await ctx.send(embed=em)

    @commands.command(help="This command shows lyrics for a song. You input the title and the bot tries to find the lyrics for that song", extras={"category":"Search"}, usage="lyrics [song name]", description="Song lyrics command")
    @commands.check(plugin_enabled)
    async def lyrics(self, ctx, *, song):
        url = "https://some-random-api.ml/lyrics"
        song = song.replace(" ", "+")
        data = {
            "title" : song
        }

        r = requests.get(url=url, data=data).json()
        if 'error' in r:
            return await ctx.send(r['error'])
        
        em = discord.Embed(
            title=r['title'],
            description=f"{r['lyrics']}\n\n[Link on genius]({r['links']['genius']})"
        )
        em.set_author(name=r['author'])
        em.set_thumbnail(url=r['thumbnail']['genius'])
        em.color = ctx.author.color

        await ctx.send(embed=em)
    
        
def setup(client):
    client.add_cog(Search(client))
