import discord
import random
from discord import app_commands
from discord.ext import commands

from utils.message import noping, spider_gifs

class SpiderCommand(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name="spider",
        aliases=["ызшвук", "паук", "паучок"],
        description="Send spider gif in chat.",
        usage="/spider",
        help="")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    async def spider(self, ctx: commands.Context):
        if isinstance(ctx.interaction, discord.Interaction) and not ctx.interaction.response.is_done(): await ctx.defer()
        if isinstance(ctx.interaction, discord.Interaction) and ctx.interaction.response.is_done(): await ctx.interaction.followup.send(random.choice(spider_gifs), allowed_mentions=noping)
        else: await ctx.reply(random.choice(spider_gifs), allowed_mentions=noping)