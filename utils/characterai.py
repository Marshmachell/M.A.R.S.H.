import asyncio
import settings
import discord
from io import BytesIO
from PyCharacterAI.exceptions import SessionClosedError

logger = settings.logging.getLogger("bot")

async def get_answer(client, chat, author, request):
    logger.info(f"📲 ({author}): request received.")
    try:
        logger.info(f"📳 ({author}): request start processing: {request}.")
        answer = await client.chat.send_message(settings.FUN_AI_CHARACTER_ID, chat.chat_id, request)
        message = answer.get_primary_candidate().text
        await client.close_session()
    except SessionClosedError:
        logger.info("📴: session closed.")
    finally:
        await client.close_session()
        logger.info(f"📱 ({author}): answer: {message}.")
        return message, answer, client

#async def get_speech(client, chat, voice_id, author, request):
#    message, answer, client = await get_answer(client, chat, author, request)
#    primary_candidate = answer.get_primary_candidate()
#
#    speech = await client.utils.generate_speech(
#                    chat_id=answer.chat_id,
#                    turn_id=answer.turn_id,
#                    candidate_id=primary_candidate.candidate_id,
#                    voice_id=voice_id)
#    return speech, message

async def gen_speech(client, answer, voice_id):
    primary_candidate = answer.get_primary_candidate()
    speech = await client.utils.generate_speech(
        chat_id=answer.chat_id,
        turn_id=answer.turn_id,
        candidate_id=primary_candidate.candidate_id,
        voice_id=voice_id)
    return speech

async def speak(self, ctx, speech):
    voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
    audio_source = discord.PCMVolumeTransformer(
         discord.FFmpegPCMAudio(BytesIO(speech), pipe=True, executable="ffmpeg"
                                ))
    if not voice_client.is_playing():
        voice_client.play(audio_source)
        while voice_client.is_playing():
            await asyncio.sleep(0.1)