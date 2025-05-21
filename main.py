import discord
from discord.ext import commands

# Replace these with your actual values
TOKEN = "MTM3NDc5MzMyNzQ3NTU1NjQ2Mw.Gjp5Ye.nKvBZl0joIDaJ5PEimw4Sne0OvKCdg5i7NaJvM"
MOD_CHANNEL_ID = 1374797067125526538  # Replace with your mod channel ID
VERIFIED_ROLE_ID = 987654321098765432  # Optional: Replace with your Verified role ID

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.dm_messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    try:
        dm_message = (
            f"Hi {member.name}, welcome to the AFE Scholars Discord!\n\n"
            "To verify your award status and gain full access, please reply to this DM "
            "with a screenshot or photo of your AFE scholarship award notification. "
            "You may blur out any sensitive information except your name and the award confirmation.\n\n"
            "A moderator will review your submission and grant you access soon. "
            "Thank you!"
        )
        await member.send(dm_message)
    except Exception as e:
        print(f"Could not send DM to {member}: {e}")
        
@bot.event
async def on_message(message):
    # Only process DMs that are not from the bot itself
    if isinstance(message.channel, discord.DMChannel) and not message.author.bot:
        if message.attachments:
            mod_channel = bot.get_channel(MOD_CHANNEL_ID)
            if mod_channel:
                # Forward the image(s) and user info to the mod channel
                files = [await a.to_file() for a in message.attachments]
                await mod_channel.send(
                    f"Verification from {message.author} ({message.author.id}):",
                    files=files
                )
                await message.channel.send(
                    "Thank you! Your verification has been sent to the moderators. "
                    "They will review it and grant you access soon."
                )
            else:
                await message.channel.send(
                    "Sorry, there was an error forwarding your verification. "
                    "Please contact a moderator."
                )
        else:
            await message.channel.send(
                "Please send a screenshot or photo of your award notification as an attachment."
            )
    await bot.process_commands(message)

# Optional: Command for mods to assign the Verified role
@bot.command()
@commands.has_permissions(manage_roles=True)
async def verify(ctx, member: discord.Member):
    role = ctx.guild.get_role(VERIFIED_ROLE_ID)
    if role:
        await member.add_roles(role)
        await ctx.send(f"{member.mention} has been verified!")
    else:
        await ctx.send("Verified role not found.")

bot.run(TOKEN)