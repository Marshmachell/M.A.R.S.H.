import discord
from discord.ext import commands

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
		#
		if curr_score >= case_cost:
			if ctx.interaction:
				await ctx.interaction.response.send_message(f"{case['msg']}", allowed_mentions=discord.AllowedMentions.none(), ephemeral=True)
			else:
				await ctx.reply(f"{case['msg']}", allowed_mentions=discord.AllowedMentions.none(), delete_after=5)
			break
	else:
		if ctx.interaction:
			await ctx.interaction.response.send_message(f"Произошла непредвиденная ошибка, пожалуйста, "
				f"сообщите о ней <@536441049644793858> или <@567014541507035148>. Ошибка:\n`{error}`",
				allowed_mentions=discord.AllowedMentions.none(), ephemeral=True)
		else:
			await ctx.reply(f"Произошла непредвиденная ошибка, пожалуйста, "
				f"сообщите о ней <@536441049644793858> или <@567014541507035148>. Ошибка:\n`{error}`",
				allowed_mentions=discord.AllowedMentions.none())
		print(error_msg)