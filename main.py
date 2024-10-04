import discord
import asyncio
from discord.ext import commands
from flask import Flask
import webserver

# Enable intents
intents = discord.Intents.default()
intents.message_content = True  # Enable intent to read message content
intents.reactions = True  # Enable intent to track reactions
intents.members = True  # Enable intent to fetch guild members

# Create Flask app

bot = commands.Bot(command_prefix="!", intents=intents)

admin_id = "1249464506812469385"  # Replace with the admin's ID
channel_id = "1269260263404867616"  # Replace with the target channel ID for reactions
log_channel_id = "1291634327557509191"  # Replace with the channel ID for logging kicks

# Ping-pong command
@bot.command(name='ping')
async def ping_pong(ctx):
    await ctx.send('Pong!')

@bot.event
async def on_message(message):
    if message.author.id == int(admin_id) and message.channel.id == int(channel_id):
        # Start monitoring reactions for the message
        await monitor_reactions(message)

    # Allows commands to work along with on_message event
    await bot.process_commands(message)

async def monitor_reactions(message):
    await asyncio.sleep(24 * 3600)  # Wait 24 hours for reactions (86400 seconds)

    # Fetch the message again after the waiting period to get up-to-date reactions
    message = await message.channel.fetch_message(message.id)
    reactions = message.reactions
    users_reacted = set()

    for reaction in reactions:
        async for user in reaction.users():
            if not user.bot:
                users_reacted.add(user)

    # Kick members who have not reacted
    await kick_non_reactors(users_reacted, message.guild)

async def kick_non_reactors(users_reacted, guild):
    log_channel = guild.get_channel(int(log_channel_id))  # Get the channel to log kicked users
    for member in guild.members:
        if not member.bot and member not in users_reacted:
            try:
                await guild.kick(member)
                # Send a log message with the member's name in the designated log channel
                await log_channel.send(f"{member.name} has been kicked for not reacting to the admin's message.")
                print(f"Kicked {member.name} for not reacting.")
            except discord.Forbidden:
                print(f"Bot doesn't have permission to kick {member.name}.")
                await log_channel.send(f"Failed to kick {member.name}, insufficient permissions.")

webserver.keep_alive()
bot.run('MTI4NDEwNjQ3NDU4NjUwOTMyMw.G-g7Vn.YBYWRO6IvAn-ANIoj89abnRfQCImeiYqvWzD1Q')  # Replace with your bot token

