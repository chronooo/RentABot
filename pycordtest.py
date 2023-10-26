import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv("locals.env")
TOKEN = os.getenv('DISCORD_TOKEN')

bot = discord.Bot(intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")


@bot.slash_command(name="test_role", description="fuck u")
async def test_role(ctx):
    # Get the role object by name
    role = discord.utils.get(ctx.guild.roles, name="testrole")
    if role is None:
        await ctx.respond(f"The role does not exist.", ephemeral=True)
        return
    # Add the role to the user
    try:
        await ctx.author.add_roles(role)
        await ctx.respond(f"You have been assigned the role.", ephemeral=True)
    except discord.Forbidden:
        await ctx.respond("I don't have the necessary permissions to assign roles.", ephemeral=True)


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


@bot.slash_command(name = 'get that bitch', description = 'leak a bitch info')
async def get_user_id(ctx, user: discord.User):
    await ctx.respond(f"User {user.name}'s ID is {user.id}")


@bot.slash_command()
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


bot.run(TOKEN)
