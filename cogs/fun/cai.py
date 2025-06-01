import asyncio
from io import BytesIO
import settings
import discord

from utils.general import handle_errors
from discord import app_commands
from discord.ext import commands
from utils.message import Embeds, noping
from settings import AUTHORIZED_IDs
from utils.cai import get_answer, get_speech

logger = settings.logging.getLogger("bot")

class ChatAICommand(commands.Cog):
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
                await msg.reply(answer[0], allowed_mentions=noping)

    @commands.hybrid_command(name="ai",
        aliases=["аи", "фш", "ии"],
        description="Ask a question of AI Elon Mask.",
        usage="'/ai <message>'",
        help="")
    @app_commands.describe(message="Write something.")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    async def ai_text_command(self, ctx: commands.Context, *, message: str):
        if not ctx.author.id in AUTHORIZED_IDs:
            error_embed=Embeds.unauth_user_embed
            error_embed.set_thumbnail(url=self.bot.user.avatar.url)
            
            if isinstance(ctx.interaction, discord.Interaction) and not ctx.interaction.response.is_done(): await ctx.reply(embed=error_embed, allowed_mentions=noping, ephemeral=True)
            else: await ctx.send(embed=error_embed, allowed_mentions=noping)
            return
        
        try:
            if isinstance(ctx.interaction, discord.Interaction) and not ctx.interaction.response.is_done(): await ctx.defer()
            answer = await get_answer(settings.FUN_AI_TOKEN, settings.FUN_AI_CHARACTER_ID, ctx.author.name, message)
            if isinstance(ctx.interaction, discord.Interaction) and ctx.interaction.response.is_done(): await ctx.interaction.followup.send(answer[0], allowed_mentions=noping)
            else: await ctx.reply(answer[0], allowed_mentions=noping)   
        except Exception as e:
            await self.ai_text_command_error(ctx, e)

    @ai_text_command.error
    async def ai_text_command_error(self, ctx, error):
        await handle_errors(ctx, error, [
            {
				"exception": commands.MissingRequiredArgument,
				"message": f"**Missed required argument**. Enter your message."
			}
        ])

class VoiceAICommand(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name="voice",
        aliases=["мщшсу", "войс", "vc", "вйос"],
        description="Ask a question of AI Elon Mask.",
        usage="'/voice <message>'",
        help="")
    @app_commands.describe(message="Write something.")
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def ai_voice_command(self, ctx: commands.Context, *, message: str):
        try:
            if ctx.author.voice is None: raise AttributeError("user must be in vc.")

            voice_channel = ctx.author.voice.channel

            if ctx.interaction and not ctx.interaction.response.is_done():
                await ctx.interaction.response.defer()

            if ctx.guild.voice_client is not None:
                await ctx.guild.voice_client.move_to(voice_channel)
            else:
                await voice_channel.connect()

            speech = await get_speech(
                settings.TEST_AI_TOKEN,
                settings.TEST_AI_CHAR,
                settings.TEST_AI_VOICE,
                ctx.author.name,
                message
            )

            if ctx.interaction:
                await ctx.interaction.followup.send(speech[1], allowed_mentions=noping)
            else:
                await ctx.reply(speech[1], allowed_mentions=noping)

            if speech:
                voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
                audio_source = discord.PCMVolumeTransformer(
                    discord.FFmpegPCMAudio(BytesIO(speech[0]), pipe=True, executable="ffmpeg"
                ))
            
                if not voice_client.is_playing():
                    voice_client.play(audio_source)
                    while voice_client.is_playing():
                        await asyncio.sleep(0.1)
        except Exception as e:
            return await self.ai_voice_command_error(ctx, e)
    @ai_voice_command.error
    async def ai_voice_command_error(self, ctx, error):
        await handle_errors(ctx, error, [
            {
				"exception": commands.MissingRequiredArgument,
                "contains": "message",
				"message": f"**Missed required argument**. Enter your message."
			},
            {
                "exception": AttributeError,
                "contains": "user must be in vc.",
                "message": f"**Bad interaction**. You must be in any voice channel."
            }
        ])