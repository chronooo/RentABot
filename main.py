import discord
from discord.ext import commands
import csv
from dotenv import load_dotenv
import os
from aiohttp import ClientSession, TCPConnector

load_dotenv("locals.env")  # Load the environment variables from .env file

intents = discord.Intents.default()  # Create a default intents object
intents.members = True  # Enable the members intent

# Create an aiohttp session with an explicit connector
connector = TCPConnector(ssl=False)
session = ClientSession(connector=connector)

bot = commands.Bot(command_prefix="!", intents=intents, http=session)
# Replace with your CSV file path
CSV_FILE_PATH = "users.csv"

# Replace with the role name that you want to add or remove
ROLE_NAME = "RoleName"

bot_token = os.getenv('DISCORD_TOKEN')
# Read the CSV file and create a dictionary with user IDs and their parameters
def read_csv_file():
    users = {}
    with open(CSV_FILE_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            user_id = int(row[0])
            parameter = bool(int(row[1]))
            users[user_id] = parameter
    return users

# Add or remove the role based on the user's parameter
async def update_role(member):
    users = read_csv_file()
    if member.id in users:
        if users[member.id]:
            await member.add_roles(discord.utils.get(member.guild.roles, name=ROLE_NAME))
        else:
            await member.remove_roles(discord.utils.get(member.guild.roles, name=ROLE_NAME))

# Event listener for member join
@bot.event
async def on_member_join(member):
    await update_role(member)

# Event listener for member update
@bot.event
async def on_member_update(before, after):
    if before.roles != after.roles:
        await update_role(after)

# Command to send a message to all members in the server
@bot.command()
async def send_message_to_all(ctx, *, message):
    if ctx.message.author.guild_permissions.administrator:  # Check if the command invoker is an administrator
        for member in ctx.guild.members:
            try:
                await member.send(message)
            except:
                pass
        await ctx.send("Message sent to all members.")
    else:
        await ctx.send("You must be an administrator to use this command.")

# Start the bot
bot.run(bot_token)
