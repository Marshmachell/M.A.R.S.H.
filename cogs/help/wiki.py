from typing import List, Literal
import discord
import json
from discord import app_commands
from discord.ext import commands

from utils.colors import bot_color

class WikiCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(
		aliases=["w", "в"], 
		description="Shows bot commands.",
		usage="/wiki <page>",
		help="")
    async def wiki(self, ctx: commands.Context, page: Literal["capes"], cape: str):
        file_path = f"assets/wiki/minecraft/capes/{cape}.json"
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        embed = discord.Embed(
            title=f"{data.get("name")} Cape",
            description=f"**Description**:\n{data.get("description")}\n\n**Obtaining**:\n{data.get("obtaining")}",
            color=bot_color)
        java = "Yes" if data["edition"]["java"] else "No"
        embed.add_field(name="Java?:", value=f"{java}", inline=True)
        bedrock = "Yes" if data["edition"]["bedrock"] else "No"
        embed.add_field(name="Bedrock?:", value=f"{bedrock}", inline=True)
        embed.add_field(name="Texture", value=f"[**Download**](https://textures.minecraft.net/texture/{data.get("id")})", inline=True)
        embed.set_image(url=f"https://vzge.me/full/576/X-Steve?y=180&replacecape={data.get("id")}")
        try:
            if isinstance(ctx.interaction, discord.Interaction) and not ctx.interaction.response.is_done(): await ctx.defer()
            if isinstance(ctx.interaction, discord.Interaction) and ctx.interaction.response.is_done(): await ctx.interaction.followup.send(embed=embed)
            else: await ctx.reply(embed=embed)
        except Exception as e:
            return print(str(e))