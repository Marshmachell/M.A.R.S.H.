import discord

from utils.colors import error_color, warn_color

noping=discord.AllowedMentions.none()

class Embeds:
    unauth_user_embed=discord.Embed(
        title='❗ Unauthorized User Detected.',
        description='You do not seem to be on the list of trusted. If an error occurs, write <@539054518885679126> about this.',
        color=error_color
    )

    mcs_error_embed=discord.Embed(
        title='❗ An Error Occurred.',
        description='Invalid address value. Try something else.',
        color=error_color)
    
    wip_embed=discord.Embed(
        title="🛠 Work In Progress.",
        description="This function currently is WIP. Check updates.",
        color=warn_color
    )