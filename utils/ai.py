import settings
from PyCharacterAI import get_client
from PyCharacterAI.exceptions import SessionClosedError

logger = settings.logging.getLogger("bot")

async def get_answer(token, char_id, author, request):
    logger.info(f"📲 ({author}): request received.")
    client = await get_client(token=token)
    chat, _ = await client.chat.create_chat(char_id)
    try:
        logger.info(f"📳 ({author}): request start processing: {request}.")
        answer = await client.chat.send_message(settings.FUN_AI_CHARACTER_ID, chat.chat_id, request)
        await client.close_session()
    except SessionClosedError:
        logger.info("📴: session closed.")
    finally:
        await client.close_session()
        logger.info(f"📱 ({author}): answer: {answer.get_primary_candidate().text}.")
        return answer.get_primary_candidate().text, answer, client

async def get_speech(token, char_id, voice_id, author, request):
    message, answer, client = await get_answer(token, char_id, author, request)
    primary_candidate = answer.get_primary_candidate()

    speech = await client.utils.generate_speech(
                    chat_id=answer.chat_id,
                    turn_id=answer.turn_id,
                    candidate_id=primary_candidate.candidate_id,
                    voice_id=voice_id
                )
    return speech, message