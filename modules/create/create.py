import discord
from discord.ext import commands

class Create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def haiku(self):
        return ""

    @commands.command()
    async def create(self, ctx, mediaType: str):
        if mediaType == "HAIKU":
            content = self.haiku()
            await ctx.send(content)