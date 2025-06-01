import discord
from discord import app_commands
from discord.ext import commands

from utils.general import handle_errors
from utils.message import Embeds, noping
from utils.api.mojang import MojangAPI
from utils.colors import bot_color

class MCPlayerCommand(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name="mcuser",
        aliases=["mcu", "мкю", "мцю", "user", "ьсг", "игрок"],
        description="Issues information about licensed account.",
        usage="'/mcuser <playername>'",
        help="")
    @app_commands.describe(playername="Minecraft Playername")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    async def mcuser(self, ctx: commands.Context, playername: str):
        try:
            if len(playername) > 16 or len(playername) < 3: raise AttributeError("Invalid playername")

            player = MojangAPI(playername)

            if not player.profile:
                return await self.mcuser_error(ctx, "UUID not found or API unavailable")
            else:
                embed = discord.Embed(
                    title="Minecraft Player Profile",
                    description=f"**{playername}**\n`{player.uuid}`",
                    color=bot_color
                )
                embed.add_field(name="Skin:", value=f"[**Texture**]({player.profile.skin_url})", inline=True)
                cape_url = f"[**Texture**]({player.profile.cape_url})" if player.profile.cape_url else "None"
                embed.add_field(name="Cape:", value=cape_url, inline=True)
                embed.set_image(url=f"https://vzge.me/full/832/{playername}.png?no=ears")

                try:
                    if isinstance(ctx.interaction, discord.Interaction) and not ctx.interaction.response.is_done(): await ctx.defer()
                    if isinstance(ctx.interaction, discord.Interaction) and ctx.interaction.response.is_done(): await ctx.interaction.followup.send(embed=embed, allowed_mentions=noping)
                    else: await ctx.reply(embed=embed, allowed_mentions=noping)
                except Exception as e:
                    await self.mcuser_error(ctx, e)
        except Exception as e:
            await self.mcuser_error(ctx, e)
    @mcuser.error
    async def mcuser_error(self, ctx, error):
        await handle_errors(ctx, error, [
            {
                "contains": "playername is a required argument",
                "message": f"**Missed required argument**. Enter playername."
            },
            {
                "exception": AttributeError,
                "contains": "Invalid playername",
                "message": "**Bad argument**. Playername is too long or too short."
            },
            {
                "contains": "UUID not found or API unavailable",
                "message": "**Fetch error**. UUID not found or API is currently unavailable"
            },
            {
				"exception": commands.MissingRequiredArgument,
				"message": f"Missed required argument."
			}
        ])