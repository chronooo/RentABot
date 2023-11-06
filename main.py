import asyncio
import csv
import discord
import os
from dotenv import load_dotenv
from io import StringIO
from functions import *

load_dotenv("locals.env")
TOKEN = os.getenv('DISCORD_TOKEN')
bot = discord.Bot(command_prefix="1", intents=discord.Intents.all())


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


# Save this function for updating list with new members
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


@bot.event
async def culvert_notify(message):
    if message.author == bot.user:
        return  # Ignore messages from the bot itself
    # who asked (Literally)
    user_initiated = None
    if message.content.lower() == "!culvertnotify" and is_junior(message):
        await message.channel.send("Please attach a CSV file.")
        # Store the user who initiated the command
        user_initiated = message.author
        try:
            message = await bot.wait_for('message', timeout=10)
            # Check if the user who sent the file is the same as the one who initiated the command
            if message.author == user_initiated:
                attachment = message.attachments[0]
                # Access the filename
                filename = attachment.filename
                if filename.endswith(".csv"):
                    await message.channel.send(f"Received a CSV file with the name: {filename}")
                    # Download and process the CSV file
                    csv_data = await attachment.read()
                    csv_text = csv_data.decode('utf-8')
                    # Process the CSV content
                    csv_file = StringIO(csv_text)
                    csv_reader = csv.reader(csv_file)
                    next(csv_reader)
                    for row in csv_reader:
                        if len(row) >= 11:  # Check if there are at least 11 columns
                            user_id = int(row[1])  # UserID is in the 2nd column (0-based index)
                            done_culvert = row[10]  # Done Culvert is in the 11th column (0-based index)
                            IGN = row[3]
                            if user_id:  # if user_id not blank
                                user = bot.get_user(user_id)
                                if done_culvert == "FALSE":
                                    await user.send(
                                        f"Hi just a friendly reminder to do your culvert this week on {IGN}.")
                                    print("Message sent")
                    # Now you have the "UserID" and "Done Culvert" values in user_ids and done_culverts
                    await message.channel.send("CSV data received and processed.")
                else:
                    await message.channel.send("Attach a CSV file.")
            else:
                await message.channel.send("You must be the user who initiated the command to submit the CSV file.")
        except asyncio.TimeoutError:
            await message.channel.send("Took too long or didn't follow instructions.")


bot.run(TOKEN)
