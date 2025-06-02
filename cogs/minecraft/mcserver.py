import discord
from discord import app_commands
from discord.ext import commands
from typing import Literal

from utils.general import handle_errors
from utils.message import noping
from utils.api.mcs import MinecraftServerStatusAPI
from utils.colors import bot_color

class MCServerCommand(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name="mc-server",
        aliases=["mcs", "мкс", "мцс", "сервер", "ьсы", "server"],
        description="Issues information about Java / Bedrock Minecraft server.",
        usage="/mc-server <java|bedrock> <address>",
        help="")
    @app_commands.describe(edition="Choose edition of minecraft server.", ip="IP-address of Minecraft server.")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    async def mcserver(self, ctx: commands.Context, edition: Literal["java", "bedrock"], ip: str):
        try:
            server = MinecraftServerStatusAPI(edition, ip)
            if not server._fetch_status(): return await self.mcserver_error(ctx, "Failed to fetch IP")

            embed = discord.Embed(title=f'Server: {server.host}', color=bot_color)
            embed.set_thumbnail(url=server.icon)
            status = '🟢 Online' if server.is_online else '🔴 Offline'
            embed.add_field(name='Status', value=f'`{status}`', inline=True)
            if (server.is_online): embed.add_field(name='Players', value=f'`{server.online}/{server.max_online}`', inline=True)
            if (server.is_online): embed.add_field(name='Version', value=f'`{server.version}`', inline=True)
            if (server.is_online): embed.add_field(name='IP-address', value=f'`{server.ip}`', inline=True)
            embed.add_field(name='Port', value=f'`{server.port}`', inline=True)
            embed.add_field(name='Full address', value=f'`{server.host}:{server.port}`', inline=True)
            if (server.is_online): embed.add_field(name='MOTD:', value=f"`{server.motd_clean}`", inline=False)

            await ctx.reply(embed=embed, allowed_mentions=noping)
        except Exception as e:
            await self.mcserver_error(ctx, e)

    @mcserver.error
    async def mcserver_error(self, ctx, error):
        await handle_errors(ctx, error, [
            {
                "contains": "edition is a required argument",
                "message": f"**Missed required argument**. Enter server edition."
            },
            {
                "contains": "ip is a required argument",
                "message": f"**Missed required argument**. Enter server IP."
            },
            {
				"exception": commands.MissingRequiredArgument,
				"message": f"Missed required argument."
			},
            {
				"contains": 'Could not convert "edition"',
				"message": "**Bad argument**. Edition must be one of: java, bedrock."
			},
            {
				"contains": "Failed to fetch IP",
				"message": "**Bad argument**. Failed to fetch IP."
			}
        ])