from typing import List
import discord
from discord import app_commands
from discord.ext import commands

from utils.colors import bot_color
from utils.message import noping
from utils.validator import list_closest_match, list_all_valid

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
		aliases=["h", "?", "х", "хелп", "помощь", "рудз"], 
		description="Shows bot commands.",
		usage="/help <command>",
		help="")
    async def help(self, ctx, *, feature=None):
        fetched_commands = await self.bot.tree.fetch_commands()
        cmd_list = [command.name for command in fetched_commands]
        if feature == None:
            permed_cmd_list = []
            for command in fetched_commands:
                permed_cmd_list.append(command)
            cmd_mentions = ", ".join([f"{command.mention}" for command in sorted(permed_cmd_list, key=lambda command: command.name)])
            embed = discord.Embed(color=bot_color)
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.description = f"## Command List:\n{cmd_mentions}\n"
            await ctx.reply(embed=embed, allowed_mentions=noping)
            return
        feature = list_closest_match(feature, cmd_list, 10)
        embed = discord.Embed(color=bot_color)
        for command in self.bot.commands:
            if feature == command.name or feature in command.aliases:
                mention = f"**/{command.name}**"
                for cmd in fetched_commands:
                    if command.name == cmd.name:
                        mention = cmd.mention
                aliases = ", ".join(f"`{alias}`" for alias in command.aliases)
                embed.description = f"## Command {mention}\n{command.description}\n### Aliases:\n{aliases}\n### Usage:\n`{command.usage}`\n\n{command.help}"
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                await ctx.reply(embed=embed, allowed_mentions=noping)
                return
    @help.autocomplete("feature")
    async def help_autocomplete(self, ctx: discord.Interaction, curr: str) -> List[app_commands.Choice[str]]:
        fetched_commands = await self.bot.tree.fetch_commands()
        cmd_list = [command.name for command in fetched_commands]

        if curr != "":
            return [app_commands.Choice(name=feature, value=feature) for feature in list_all_valid(curr, cmd_list)][:25]
        else:
            return [app_commands.Choice(name=feature, value=feature) for feature in cmd_list][:25]