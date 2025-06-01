import discord
from discord.ext import commands

from utils.message import Embeds

async def handle_errors(ctx, error, errors):
	if isinstance(ctx, discord.Interaction):
		ctx = await commands.Context.from_interaction(ctx)
	error_msg = str(error)
	for case in errors:
		case_cost = len(case) - 1
		curr_score = 0
		if "exception" in case and isinstance(error, case["exception"]):
			curr_score += 1
		if "contains" in case and case["contains"] in error_msg:
			curr_score += 1
			
		if curr_score >= case_cost:
			embed = Embeds.error_embed
			embed.description = f"{case['message']}"
			if ctx.interaction:
				embed.set_thumbnail(url=ctx.bot.user.avatar.url)
				await ctx.interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions.none(), ephemeral=True)
			else:
				embed.set_thumbnail(url=ctx.bot.user.avatar.url)
				await ctx.reply(embed=embed, allowed_mentions=discord.AllowedMentions.none(), delete_after=5)
			break
	else:
		if ctx.interaction:
			await ctx.interaction.response.send_message(f"An unforeseen error occurred, "
				f"please inform about it <@539054518885679126>. Error:\n`{error}`",
				allowed_mentions=discord.AllowedMentions.none(), ephemeral=True)
		else:
			await ctx.reply(f"An unforeseen error occurred, "
				f"please inform about it <@539054518885679126>. Error:\n`{error}`",
				allowed_mentions=discord.AllowedMentions.none())
		print(error_msg)