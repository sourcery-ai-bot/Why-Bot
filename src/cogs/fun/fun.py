import io
import os
import random
import asyncio
import tempfile
import textwrap

import discord
import validators
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

import __main__
from core import BaseCog, WhyBot
from core.helpers import RickRollView


class Fun(BaseCog):
    def __init__(self, client: WhyBot) -> None:
        path = os.path.join(
            os.path.dirname(__main__.__file__), "../assets/images/spongebob"
        )
        images = {}
        for image in os.listdir(path):
            key = image.split(".")[0]
            images[key] = image

        self.spongebob_images = images
        self.spongebob_path = path

        super().__init__(client)

    @staticmethod
    async def gen_crab(t1: str, t2: str, ctx: discord.ApplicationContext):
        path = os.path.join(
            os.path.dirname(__main__.__file__).replace("src", ""),
            "assets/videos/crab.mp4",
        )
        clip = VideoFileClip(path)
        text = TextClip(t1, fontsize=48, color="white", font="Symbola")
        text2 = (
            TextClip("____________________", fontsize=48, color="white", font="Verdana")
            .set_position(("center", 210))
            .set_duration(15.4)
        )
        text = text.set_position(("center", 200)).set_duration(15.4)
        text3 = (
            TextClip(t2, fontsize=48, color="white", font="Verdana")
            .set_position(("center", 270))
            .set_duration(15.4)
        )

        video = CompositeVideoClip(
            [clip, text.crossfadein(1), text2.crossfadein(1), text3.crossfadein(1)]
        ).set_duration(15.4)
        file = tempfile.NamedTemporaryFile(suffix=".mp4")
        video.write_videofile(file.name, threads=4, preset="superfast", verbose=False)
        clip.close()
        video.close()
        file.seek(0)
        await ctx.respond(file=discord.File(file.name, "crab.mp4"))
        file.close()

    async def gen_spongebob(
        self,
        number: int,
        unit: str,
        ctx: discord.ApplicationContext,
        background: str,
        color: str,
    ):
        path = os.path.join(self.spongebob_path, background)
        font_path = os.path.join(
            os.path.dirname(__main__.__file__), "../assets/fonts/Some_Time_Later.otf"
        )
        font = ImageFont.truetype(font_path, 100)
        image = Image.open(path)
        draw = ImageDraw.Draw(image)
        text = f"{number} {unit} Later..."
        para = textwrap.wrap(text, width=30)
        width, height = image.size
        current_h, pad = height // 2, 10
        for line in para:
            w, h = draw.textsize(line, font=font)
            try:
                draw.text(((width - w) / 2, current_h), line, font=font, fill=color)
            except ValueError:
                draw.text(((width - w) / 2, current_h), line, font=font, fill=color)
                color = "white"
            current_h += h + pad
        file = io.BytesIO()
        image.save(file, "PNG")
        file.seek(0)
        await ctx.respond(file=discord.File(file, "spongebob.png"))

    @commands.slash_command(description="Generate a crab rave meme video")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def crab(self, ctx: discord.ApplicationContext, text1: str, text2: str):
        await ctx.defer()
        asyncio.create_task(self.gen_crab(text1, text2, ctx))

    @commands.slash_command(description="Claim your why coins")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def claim(self, ctx: discord.ApplicationContext):
        em = discord.Embed(title="Claim 100k Why Coins", color=discord.Color.blue())
        await ctx.respond(embed=em, view=RickRollView(self.client.db))

    @commands.slash_command(description="Generate a spongebob timecard")
    async def spongebob(
        self,
        ctx: discord.ApplicationContext,
        number: int,
        unit: str,
        background: discord.Option(
            str,
            default="bamboo",
            choices=[
                "title",
                "flowers",
                "heads",
                "purplewood",
                "blueseaweed",
                "wood",
                "tiles",
                "seaweed",
                "sand",
                "steel",
                "crosshatch",
                "greenseaweed",
                "bamboo",
            ],
        ),
        color: str = "white",
    ):
        await ctx.defer()
        self.client.loop.create_task(
            self.gen_spongebob(
                number, unit, ctx, self.spongebob_images[background], color
            )
        )

    @commands.slash_command(
        name="8ball", description="Ask the magical 8ball a question"
    )
    async def _8ball(self, ctx: discord.ApplicationContext, question: str):
        responses = [
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
            "Very doubtful",
            "Yes",
            "No",
            "Never",
            "Definitely",
            "Ask again later",
            "Does Siri know the answer?",
            "What do you think?",
            "Wait, what say that again",
            "roll again",
            "maybe ;)",
            "stop",
            "I don't understand you",
            "Speak clearer",
            "Does Alexa know the answer?",
            "Think about it",
            "Yeah, obviously",
            "No... Yes",
            "That's obviously a yes",
            "There's an obvious answer, why are you asking me this?",
            "Literally yes",
            "Why are you asking me this?",
            "Yeahhhh",
            "I *totally* understand",
            "L(%)/",
            "When you think about it... the answer is yes",
            "When you think about it..",
            "the answer is no",
            "When you think about it... the answer is so obvious",
            "the answer is yes",
            "the answer is no",
            "I'm busy, ask me that later",
            "That's not important right now",
            "lol",
            "good question",
        ]
        em = discord.Embed(
            title="8 Ball 🎱",
            description=(
                f"**Question:** {question}\n**Answer:** {random.choice(responses)}"
            ),
            color=ctx.author.color,
        )
        await ctx.respond(embed=em)

    @commands.slash_command(description="Do a 100% legit hack on another member")
    async def hack(self, ctx: discord.ApplicationContext, member: discord.Member):
        await ctx.defer()
        email_ext = [
            "gmail.com",
            "yahoo.com",
            "hotmail.com",
            "aol.com",
            "hotmail.co.uk",
            "hotmail.fr",
            "msn.com",
            "yahoo.fr",
            "wanadoo.fr",
            "orange.fr",
            "comcast.net",
            "yahoo.co.uk",
            "yahoo.com.br",
            "yahoo.co.in",
            "live.com",
            "rediffmail.com",
            "free.fr",
            "gmx.de",
            "web.de",
            "yandex.ru",
            "ymail.com",
            "libero.it",
            "outlook.com",
            "uol.com.br",
            "bol.com.br",
            "mail.ru",
            "cox.net",
            "hotmail.it",
            "sbcglobal.net",
            "sfr.fr",
            "live.fr",
            "verizon.net",
            "live.co.uk",
        ]
        most_used_words = [
            "TrASh",
            "gEt gUd",
            "waSsUp",
            "noOb",
            "LmAo",
            "lol",
            "lMfao",
            "e",
            "seNd nUkeS",
            "f&Ck",
            "sH#t",
            "nub",
            "b1T#h",
        ]
        passwords = [
            "123456",
            "password",
            "12345",
            "123456789",
            "password1",
            "abc123",
            "12345678",
            "qwerty",
            "111111",
            "1234567",
            "1234",
            "iloveyou",
            "sunshine",
            "monkey",
            "1234567890",
            "123123",
            "princess",
            "baseball",
            "dragon",
            "football",
            "shadow",
            "michael",
            "soccer",
            "unknown",
            "maggie",
            "000000.",
            "ashley",
            "myspace1",
            "purple",
            "fuckyou",
            "charlie",
            "jordan",
            "hunter",
            "superman",
            "tigger",
            "michelle",
            "buster",
            "pepper",
            "justin",
            "andrew",
            "harley",
            "matthew",
            "bailey",
            "jennifer",
            "samantha",
            "ginger",
            "anthony",
            "qwerty123",
            "qwerty1",
            "peanut",
        ]

        hack_message = await ctx.send(f"[▖] Hacking {member.display_name} now...")
        await asyncio.sleep(1.420)
        await hack_message.edit(content="[▘] Finding discord login... (2fa bypassed)")
        await asyncio.sleep(1.69)
        email = (
            f"{member.display_name}.{random.randint(1, 100)}@{random.choice(email_ext)}"
        )
        await hack_message.edit(
            content=f"[▝] `Email: {email}`\n    `Password: {random.choice(passwords)}`"
        )
        await asyncio.sleep(1.420)
        await hack_message.edit(content="[▗] IP address: 127.0.0.1:50")
        await asyncio.sleep(1.69)
        await hack_message.edit(
            content=f"[▖] Most used words: {random.choice(most_used_words)}"
        )
        await asyncio.sleep(1.420)
        await hack_message.edit(
            content=(
                f"[▘] Injecting trojan virus into discriminator: {member.discriminator}"
            )
        )
        await asyncio.sleep(1.69)
        await hack_message.edit(content="[▝] Selling information to the government...")
        await asyncio.sleep(1.420)
        await hack_message.edit(
            content="[▗] Reporting account to discord for breaking TOS..."
        )
        await asyncio.sleep(1.69)
        await hack_message.edit(content="[▖] Hacking medical records...")
        await asyncio.sleep(1.420)
        await hack_message.edit(content=f"Finished hacking {member.mention}")

        await ctx.respond("The *totally* real and dangerous hack is complete!")

    @commands.slash_command(
        description="Display a screenshot of the page at the given link"
    )
    async def screenshot(self, ctx: discord.ApplicationContext, url: str):
        if not validators.url(url):
            return await ctx.respond("Not a url", ephemeral=True)

        em = discord.Embed(
            title="Screenshot", description=f"[Link]({url})", color=ctx.author.color
        )
        em.set_image(url=f"https://image.thum.io/get/{url}")
        await ctx.respond(embed=em)


def setup(client):
    client.add_cog(Fun(client))
