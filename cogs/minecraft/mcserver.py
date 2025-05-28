import discord
from discord import app_commands
from discord.ext import commands
from typing import Literal

from utils.general import handle_errors
from utils.message import Embeds
from utils.mcs import MinecraftServerStatus
from utils.colors import bot_color

class MCServerCommand(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name="mc-server",
        aliases=["mcs", "мкс", "мцс", "сервер", "ьсы", "server"],
        description="Issues information about Java / Bedrock server.",
        usage="'/mc-server <java|bedrock> <адрес>'",
        help="")
    @app_commands.describe(edition="Choose edition of minecraft server.", ip="IP-address of Minecraft server.")
    async def mcserver(self, ctx, edition: Literal["java", "bedrock"], ip: str):
        server = MinecraftServerStatus(edition, ip)
        
        if (server._fetch_status()):
            embed = discord.Embed(title=f'Server: {server.host}', color=bot_color)
            embed.set_thumbnail(url=server.icon)
            embed.add_field(name='Status', value=f'`{'🟢 Online' if server.is_online else '🔴 Offline'}`', inline=True)
            if (server.is_online): embed.add_field(name='Players', value=f'`{server.online}/{server.max_online}`', inline=True)
            if (server.is_online): embed.add_field(name='Version', value=f'`{server.version}`', inline=True)
            if (server.is_online): embed.add_field(name='IP-address', value=f'`{server.ip}`', inline=True)
            embed.add_field(name='Port', value=f'`{server.port}`', inline=True)
            embed.add_field(name='Full address', value=f'`{server.host}:{server.port}`', inline=True)
            if (server.is_online): embed.add_field(name='MOTD:', value=f"`{server.motd_clean}`", inline=False)

            await ctx.reply(embed=embed, allowed_mentions=discord.AllowedMentions.none())
        else:
            error_embed=Embeds.mcs_error_embed
            error_embed.set_thumbnail(url=self.bot.user.avatar.url)
            await ctx.reply(embed=error_embed, allowed_mentions=discord.AllowedMentions.none())

    @mcserver.error
    async def mcserver_error(self, ctx, error: Exception):
        await handle_errors(ctx, error, [
            {
				"contains": "'NotFound'",
				"msg": "NotFound"
			}
        ])