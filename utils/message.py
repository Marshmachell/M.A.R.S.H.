import discord

from utils.colors import error_color, warn_color

noping=discord.AllowedMentions.none()

spider_gifs = [
    "https://tenor.com/view/eww-a-spider-gif-25352428",
    "https://tenor.com/view/spider-insects-gif-5885471679186248700",
    "https://tenor.com/view/crab-spider-mexican-dance-gif-25806854",
    "https://tenor.com/view/spider-scary-sleeping-huge-sleep-gif-6188742989761831337",
    "https://tenor.com/view/spider-spider-dance-dance-spiderdance-spider-costumer-gif-14357114683293314026",
    "https://tenor.com/view/spider-on-wall-terrifying-spider-spider-crawling-spider-crawling-up-wall-itsy-bitsy-spider-gif-15199577248523327627",
    "https://tenor.com/view/spiders-spider-creepy-pictures-creepy-gif-11183740927637194229"
]

class Embeds:
    error_embed=discord.Embed(
        title='❗ An Error Occurred.',
        color=error_color)
    
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