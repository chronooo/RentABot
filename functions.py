import csv
import discord
import os
from dotenv import load_dotenv


def is_junior(ctx):
    junior = discord.utils.get(ctx.guild.roles, name="Matcha - Juniors") in ctx.author.roles
    return junior



