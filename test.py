# bot.py
#pip install discord.py version
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv("locals.env")
TOKEN = os.getenv('DISCORD_TOKEN')

# Define the intents your bot needs
intents = discord.Intents.default()
intents.guilds = True

# Create a bot instance with the specified intents
bot = commands.Bot(command_prefix="/", description="Hello Bot", intents=intents)

# Define a simple slash command
@bot.slash_command(
    name="hello",
    description="Responds with Hello!"
)
async def hello(ctx: discord.SlashContext):
    await ctx.send("Hello!")


# Run the bot with your bot token
bot.run(TOKEN)
