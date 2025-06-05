import settings
import discord
from discord.ext import commands
from PyCharacterAI import get_client

from cogs.general import BotPing
from cogs.minecraft import MCServerCommand, MCPlayerCommand
from cogs.fun import ChatAICommand, VoiceAICommand, SpiderCommand
from cogs.help import HelpCommand, WikiCapesCommand

logger = settings.logging.getLogger("bot")

cogs = [BotPing, HelpCommand, MCServerCommand, MCPlayerCommand, ChatAICommand, VoiceAICommand, WikiCapesCommand, SpiderCommand]


token=settings.FUN_CAI_TOKEN
char_id=settings.FUN_CAI_CHARACTER_ID


class MarshBot(commands.Bot):
    def __init__(self, *, intents: discord.Intents, command_prefix: str):
        super().__init__(intents=intents, command_prefix=commands.when_mentioned_or(command_prefix), case_insensitive=True)
        self.ai_char_id = char_id

    async def setup_hook(self):
        self.remove_command("help")
        for cog in cogs:
            await self.add_cog(cog(self))
        await self.tree.sync()
        HelpCog = self.get_cog("HelpCommand")
        self.ai_client = await get_client(token=token)
        account = await self.ai_client.account.fetch_me()
        self.ai_chat, g = await self.ai_client.chat.create_chat(char_id)

        logger.info(f"🤖: {bot.user.name} | 👦: {account.name} | 👤: {g.author_name}")
        try:
            with open("assets/images/bot.png", "rb") as file:
                await bot.user.edit(avatar=file.read())
        except:
            logger.warning("pfp ratelimit")
                
intents = discord.Intents.all()
bot = MarshBot(command_prefix=settings.COMMAND_PREFIX, intents=intents)

bot.run(settings.DISCORD_API_SECRET, root_logger=True)