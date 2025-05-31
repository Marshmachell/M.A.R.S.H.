import settings
import discord
from discord.ext import commands

from cogs.general import BotPing
from cogs.minecraft import MCServerCommand
from cogs.fun import ChatAICommand, VoiceAICommand

logger = settings.logging.getLogger("bot")

cogs = [BotPing, MCServerCommand, ChatAICommand, VoiceAICommand]

class MarshBot(commands.Bot):
    def __init__(self, *, intents: discord.Intents, command_prefix: str):
        super().__init__(intents=intents, command_prefix=commands.when_mentioned_or(command_prefix), case_insensitive=True)

    async def setup_hook(self):
        self.remove_command("help")
        for cog in cogs:
            await self.add_cog(cog(self))
        await self.tree.sync()

        logger.info(f"🤖: {bot.user.name}")
        try:
            with open("assets/images/bot.png", "rb") as file:
                await bot.user.edit(avatar=file.read())
        except:
            logger.warning("pfp ratelimit")
                
intents = discord.Intents.all()
bot = MarshBot(command_prefix=settings.COMMAND_PREFIX, intents=intents)

bot.run(settings.DISCORD_API_SECRET, root_logger=True)