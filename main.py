from functions import *
import csv
import discord
import os
from dotenv import load_dotenv

load_dotenv("locals.env")
TOKEN = os.getenv('DISCORD_TOKEN')
bot = discord.Bot(intents=discord.Intents.all())

global culvert_wait
culvert_wait = 0

def update_wait():
    global culvert_wait
    if culvert_wait == 0:
        culvert_wait = 1
    else:
        culvert_wait = 0
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="remove_role", description="fuck u")
async def remove_role(ctx):
    # Get the role object by name
    role = discord.utils.get(ctx.guild.roles, name="testrole")
    if role is None:
        await ctx.respond(f"The role does not exist.", ephemeral=True)
        return
    # Add the role to the user
    try:
        await ctx.author.remove_roles(role)
        await ctx.respond(f"You have been removed the role.", ephemeral=True)
    except discord.Forbidden:
        await ctx.respond("I don't have the necessary permissions to assign roles.", ephemeral=True)


@bot.slash_command(name="get_that_bitch", description="leak a bitch info")
async def get_user_id(ctx, user: discord.User):
    await ctx.respond(f"User {user.name}'s ID is {user.id}")


@bot.slash_command(name="harass", description="FRIENDLY REMINDER FOR CULVERT")
async def send_message(ctx):
    user_list = [128442423323000832]
    should_send_message = True
    if should_send_message:
        for user_id in user_list:
            user = bot.get_user(user_id)
            if user:
                try:
                    await user.send("Fuck you do culvert")
                except discord.Forbidden:
                    await ctx.send(f"Couldn't send a message to {user.name}.")
            else:
                await ctx.send(f"User with ID {user_id} not found.")
    else:
        await ctx.send("The condition is not met, so no messages were sent.")


@bot.slash_command(name="export-names", description="doxx everyone")
async def export_members(ctx):
    # Fetch the specific role by name
    if is_junior(ctx):
        specific_role = discord.utils.get(ctx.guild.roles, name="Oolong - Guild Member")
        if specific_role is None:
            await ctx.respond(f"The role {specific_role} does not exist in this server.")
            return

        # Get members who have the specific role
        members_with_specific_role = [member for member in ctx.guild.members if specific_role in member.roles]

        # Create a CSV file with usernames and user IDs of members with the specific role
        with open("members_with_specific_role.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "UserID"])
            for member in members_with_specific_role:
                writer.writerow([member.name, member.id])

        # Send the CSV file to the command invoker
        with open("members_with_specific_role.csv", "rb") as file:
            await ctx.author.send(file=discord.File(file, "members_with_specific_role.csv"))

        await ctx.respond(f"Member information with the '{specific_role}' role exported and sent to your DMs.")
    else:
        ctx.respond("You cant use this command", ephemeral=True)


@bot.slash_command()
async def test_matcha(ctx):
    if is_junior(ctx):
        await ctx.send("You are in fact a junior")
    else:
        await ctx.send("agony awaits")


#
# @bot.slash_command(name="culvert_check", description="Return a list of who hasn't done culvert")
# async def process_file(ctx, uploaded_file: discord.File):
#     # Check if a file is attached
#     if uploaded_file:
#         # Get information about the uploaded file
#         file_info = f"File Name: {uploaded_file.filename}\nFile Size: {uploaded_file.filesize} bytes"
#         await ctx.send(f"Received a file!\n{file_info}")
#     else:
#         await ctx.send("No file attached. Please attach a file for processing.")


@bot.event
async def on_message(message):
    global culvert_wait
    # Check if the message sender is not the bot itself to avoid an infinite loop
    if message.author == bot.user:
        return

    if is_junior(message) and message.content == "!culvert notify":
        await message.channel.send("Alrighty waiting for the csv file")
        update_wait()

    if culvert_wait == 1 and len(message.attachments) == 1:
        if message.attachments and is_junior(message):
            for attachment in message.attachments:
                await message.channel.send(f"File Name: {attachment.filename}")
                # Get the current working directory
                current_directory = os.getcwd()
                # Form the file path for saving in the current directory
                file_path = os.path.join(current_directory, attachment.filename)
                print(file_path)
                await attachment.save(file_path)
                await message.channel.send("Saved file")

        else:
            await message.channel.send("No files in the message, no longer waiting")
            culvert_wait = 0


bot.run(TOKEN)
