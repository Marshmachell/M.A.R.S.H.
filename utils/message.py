import discord

from utils.colors import error_color, warn_color

noping=discord.AllowedMentions.none()

class Embeds:
    mcs_error_embed=discord.Embed(
        title='❗ An Error Occurred.',
        description='Invalid address value. Try something else.',
        color=error_color)
    
    wip_embed=discord.Embed(
        title="🛠 Work In Progress.",
        description="This function currently is WIP. Check updates.",
        color=warn_color
    )