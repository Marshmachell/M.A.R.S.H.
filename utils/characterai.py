import asyncio

import PyCharacterAI.types
import settings
import discord
import PyCharacterAI
from typing import NamedTuple, Optional
from io import BytesIO
from PyCharacterAI.exceptions import SessionClosedError

logger = settings.logging.getLogger("bot")

class AIChatResponse(NamedTuple):
    client: PyCharacterAI.client.AsyncClient
    chat: PyCharacterAI.types.chat.Chat
    answer: PyCharacterAI.types.message.Turn
    message: str

class AIChatHandler:
    def __init__(self, char_id):
        self._response: Optional[AIChatResponse] = None
        self.char_id = char_id

    async def send_request(self, client, chat, author, request, log: bool):
        if log: logger.info(f"📲 ({author}): request received.")
        try:
            if log: logger.info(f"📳 ({author}): request start processing: {request}.")
            answer = await client.chat.send_message(self.char_id, chat.chat_id, request)
            message = answer.get_primary_candidate().text
            await client.close_session()
        except SessionClosedError:
            if log: logger.info("📴: session closed.")
        finally:
            await client.close_session()
            if log: logger.info(f"📱 ({author}): answer: {message}.")

        self._response = AIChatResponse(client, chat, answer, message)
        return self._response
    
    @property
    def chat(self) -> PyCharacterAI.types.chat.Chat:
        return self._response.chat if self._response is not None else ValueError("'missed send_request()'")

    @property
    def message(self) -> str:
        return self._response.message if self._response is not None else ValueError("'missed send_request()'")
    
    @property
    def answer(self) -> PyCharacterAI.types.message.Turn:
        return self._response.answer if self._response is not None else ValueError("'missed send_request()'")
    
    @property
    def client(self) -> PyCharacterAI.client.AsyncClient:
        return self._response.client if self._response is not None else ValueError("'missed send_request()'")

async def gen_speech(client, answer, voice_id):
    primary_candidate = answer.get_primary_candidate()
    speech = await client.utils.generate_speech(
        chat_id=answer.chat_id,
        turn_id=answer.turn_id,
        candidate_id=primary_candidate.candidate_id,
        voice_id=voice_id)
    return speech

async def speak(speech, vc: discord.VoiceClient):
    audio_source = discord.PCMVolumeTransformer(
         discord.FFmpegPCMAudio(BytesIO(speech), pipe=True, executable="ffmpeg"
                                ))
    if not vc.is_playing():
        vc.play(audio_source)
        while vc.is_playing():
            await asyncio.sleep(0.1)