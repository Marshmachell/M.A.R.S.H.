from PIL import Image
import requests
from io import BytesIO
import discord
from discord import app_commands
from discord.ext import commands
import json

from utils.general import handle_errors
from utils.message import noping
from utils.api.mojang import MojangAPI
from utils.colors import bot_color

async def combine(name):
    front = f"https://vzge.me/full/832/{name}.png?y=0"
    back = f"https://vzge.me/full/832/{name}.png?y=180"
    
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    try:
        response1 = requests.get(front, headers=headers, timeout=10)
        response2 = requests.get(back, headers=headers, timeout=10)
        
        if response1.status_code != 200 or response2.status_code != 200:
            return None
        
        img1 = Image.open(BytesIO(response1.content))
        img2 = Image.open(BytesIO(response2.content))
        
        new_width = img1.width + img2.width
        new_height = max(img1.height, img2.height)
        new_img = Image.new('RGBA', (new_width, new_height))
        
        new_img.paste(img1, (0, 0))
        new_img.paste(img2, (img1.width, 0))
        
        buffer = BytesIO()
        new_img.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        print(f"Error: {e}")
        return None

class MCPlayerCommand(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name="mc-player",
        aliases=["mcu", "мкю", "мцю", "user", "ьсг", "игрок"],
        description="Issues information about licensed minecraft account.",
        usage="/mc-player <name>",
        help="")
    @app_commands.describe(playername="Minecraft username.")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    async def mcuser(self, ctx: commands.Context, playername: str):
        try:
            if len(playername) > 16 or len(playername) < 3: raise AttributeError("Invalid playername")

            player = MojangAPI(playername)

            if not player.profile:
                return await self.mcuser_error(ctx, "UUID not found or API unavailable")
            else:
                image = await combine(player.profile.name)

                embed = discord.Embed(
                    title="Minecraft Player Profile",
                    description=f"**{player.profile.name}**\n`{player.uuid}`",
                    color=bot_color
                )
                embed.add_field(name="Skin:", value=f"[**Texture**]({player.profile.skin_url})", inline=True)
                cape_url = f"[**Texture**]({player.profile.cape_url})" if player.profile.cape_url else "None"
                embed.add_field(name="Cape:", value=cape_url, inline=True)
                embed.set_thumbnail(url=f"https://vzge.me/face/64/{player.profile.name}.png?no=ears")

                if image:
                    file = discord.File(image, filename=f"skin_combined.png")
                    embed.set_image(url=f"attachment://skin_combined.png")
                else:
                    embed.set_image(url=f"https://vzge.me/full/832/{player.profile.name}.png")
                    file = None

                try:
                    if isinstance(ctx.interaction, discord.Interaction) and not ctx.interaction.response.is_done(): await ctx.defer()
                    if isinstance(ctx.interaction, discord.Interaction) and ctx.interaction.response.is_done(): await ctx.interaction.followup.send(embed=embed, file=file, allowed_mentions=noping)
                    else: await ctx.reply(embed=embed, file=file, allowed_mentions=noping)
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