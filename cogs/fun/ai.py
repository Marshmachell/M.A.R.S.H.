import settings
import discord

from utils.general import handle_errors
from discord import app_commands
from discord.ext import commands
from utils.message import Embeds, noping
from settings import AUTHORIZED_IDs

from PyCharacterAI import get_client
from PyCharacterAI.exceptions import SessionClosedError

logger = settings.logging.getLogger("bot")

async def get_answer(token, char_id, author, request):
    logger.info(f"📲 ({author}): request received.")
    client = await get_client(token=token)
    chat, g = await client.chat.create_chat(char_id)
    try:
        logger.info(f"📳 ({author}): request processing: {request}.")
        answer = await client.chat.send_message(settings.FUN_AI_CHARACTER_ID, chat.chat_id, request)
        await client.close_session()
    except SessionClosedError:
        logger.info("📴: session closed.")
    finally:
        await client.close_session()
        logger.info(f"📱 ({author}): answer: {answer.get_primary_candidate().text}.")
        return answer.get_primary_candidate().text

class AICommand(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener("on_message")
    async def ai_text(self, msg):
        if msg.author == self.bot.user: return
        if not msg.author.id in AUTHORIZED_IDs:
            return
        else:
            if (msg.reference.resolved.author.id == 1286298001756782665 if msg.reference else None or msg.channel.type == discord.ChannelType.private and not msg.content.startswith(settings.COMMAND_PREFIX)):
                answer = await get_answer(settings.FUN_AI_TOKEN, settings.FUN_AI_CHARACTER_ID, msg.author.name, msg.content)
                await msg.reply(answer, allowed_mentions=noping)

    @commands.hybrid_command(name="ai",
        aliases=["аи", "фш", "ии"],
        description="Ask a question of AI Elon Mask.",
        usage="'/ai <message>'",
        help="")
    @app_commands.describe(message="Write something.")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    async def ai_command(self, ctx, *, message: str):
        if not ctx.author.id in AUTHORIZED_IDs:
            error_embed=Embeds.unauth_user_embed
            error_embed.set_thumbnail(url=self.bot.user.avatar.url)
            await ctx.reply(embed=error_embed, allowed_mentions=noping, ephemeral=True)
            return
        else:
            await ctx.defer()
            answer = await get_answer(settings.FUN_AI_TOKEN, settings.FUN_AI_CHARACTER_ID, ctx.author.name, message)
            await ctx.reply(answer, allowed_mentions=noping)
    @ai_command.error
    async def ai_command_error(self, ctx, error):
        await handle_errors(ctx, error, [
            {
				"exception": commands.MissingRequiredArgument,
				"msg": f"Write a message that you want to send Elon AI."
			}
        ])