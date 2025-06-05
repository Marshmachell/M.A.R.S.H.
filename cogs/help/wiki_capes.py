from typing import List
import discord
import json
import os
from discord import app_commands
from discord.ext import commands

from utils.colors import bot_color
from utils.validator import dict_all_valid

def capes_dict() -> dict[str, str]:
    directory = "assets/wiki/minecraft/capes"
    cape_dict = {}
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    name = data.get("name")
                    if name:
                        cape_dict[name] = filename[:-5]
            except (json.JSONDecodeError, KeyError, UnicodeDecodeError, FileNotFoundError) as e:
                print(f"Error. {filename}: {e}")
    return cape_dict

class WikiCapesCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(
        name="wiki-capes",
        description="Shows information about Minecraft cape.",
    )
    @app_commands.describe(cape="Cape name.")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    async def wiki_capes(self, ctx: commands.Context, cape: str):
        try:
            capes = capes_dict()
            file_path = f"assets/wiki/minecraft/capes/{capes[cape]}.json"
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            embed = discord.Embed(
                title=f"{data.get('name', 'Unknown')} Cape",
                description=f"**Description**:\n{data.get('description', 'No description')}\n\n**Obtaining**:\n{data.get('obtaining', 'No info')}",
                color=bot_color
            )
            java = "Yes" if data.get("edition", {}).get("java", False) else "No"
            bedrock = "Yes" if data.get("edition", {}).get("bedrock", False) else "No"
            embed.add_field(name="Java?:", value=java, inline=True)
            embed.add_field(name="Bedrock?:", value=bedrock, inline=True)
            embed.add_field(name="Texture", value=f"[**Download**](https://textures.minecraft.net/texture/{data.get('id', '')})", inline=True)
            embed.set_image(url=f"https://vzge.me/full/576/X-Steve?y=180&replacecape={data.get('id', '')}")

            if ctx.interaction:
                await ctx.interaction.response.send_message(embed=embed)
            else:
                await ctx.reply(embed=embed)
        except Exception as e:
            await ctx.send(f"Error: {e}", ephemeral=True)

    @wiki_capes.autocomplete("cape")
    async def cape_autocomplete(self, ctx: discord.Interaction, curr: str) -> List[app_commands.Choice[str]]:
        capes = capes_dict()
        if curr != "":
            return [app_commands.Choice(name=cape, value=cape) for cape in dict_all_valid(curr, capes)[:25]]
        else:
            return [app_commands.Choice(name=cape, value=cape) for cape in list(capes)][:25]