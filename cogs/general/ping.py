import discord
from discord.ext import commands

from utils.message import noping
from utils.colors import bot_color

class BotPing(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    async def _create_ping_embed(self, author: discord.User) -> discord.Embed:
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title=f"🏓 Pong, {author.name}!",
            description=f"Great to have you here! I’m <@{self.bot.user.id}>, a bot created by <@539054518885679126> to help out on this server.\n\n"
                       f"📌 Make sure to check out the rules in **empty** to avoid any trouble.\n"
                       f"💡 If you have any questions, feel free to ask in chat or ping the mods.\n\n"
                       f"Hope you enjoy your stay and have fun! 😊",
            color=bot_color)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text=f"🆔 {self.bot.user.id}     💻 {latency}ms")
        return embed

    @commands.Cog.listener("on_message")
    async def ping(self, msg):
        if msg.author == self.bot.user:
            return
        if msg.content == (f"<@{self.bot.user.id}>"):
            embed = await self._create_ping_embed(msg.author)
            await msg.reply(embed=embed, allowed_mentions=noping)

    @commands.hybrid_command(name="ping",
        aliases=["пинг", "gbyu", "зштп"],
        description='"Pong" message about bot.',
        usage="/ping",
        help="")
    async def ping_command(self, msg):
        embed = await self._create_ping_embed(msg.author)
        await msg.reply(embed=embed, allowed_mentions=noping)