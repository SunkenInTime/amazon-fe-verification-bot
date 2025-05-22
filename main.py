import discord
from discord.ext import commands

TOKEN = "MTM3NDc5MzMyNzQ3NTU1NjQ2Mw.Gjp5Ye.nKvBZl0joIDaJ5PEimw4Sne0OvKCdg5i7NaJvM"
MOD_CHANNEL_ID = 1374797067125526538  # Replace with your mod channel ID
VERIFIED_ROLE_ID = 1374797431216013332  # Optional: Replace with your Verified role ID
YOUR_GUILD_ID = 1374591755684548688
UNVERIFIED_ROLE = 1374797350765072449
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.dm_messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class VerificationView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    def disable_all_items(self):
            for item in self.children:  # children is a list of your buttons
                item.disabled = True

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        member = guild.get_member(self.user_id)
        role = guild.get_role(VERIFIED_ROLE_ID)
        if member and role:
            await member.add_roles(role)
            try:
                await member.send(
                    f"🎉 Congratulations, you’ve been **verified** and now have full access to the server! "
                    "We’re excited to have you here! <a:pandahappy:1374892290790654022> \n\n"
                    "Please take a moment to introduce yourself in our introductions channel: "
                    "[introductions channel](https://discord.com/channels/1374591755684548688/1374592207591444550)\n\n"
                    "Welcome to the community! 😊"
                )
            except Exception:
                pass
            await interaction.response.send_message(f"{member.mention} has been verified!", ephemeral=True)
        else:
            await interaction.response.send_message("Could not verify user (not found or role missing).", ephemeral=True)
        self.disable_all_items()
        await interaction.message.edit(view=self)

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.danger)
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        member = guild.get_member(self.user_id)
        if member:
            try:
                await member.send("❌ Your verification was rejected. Please contact a moderator if you have questions.")
            except Exception:
                pass
            await interaction.response.send_message(f"{member.mention}'s verification was rejected.", ephemeral=True)
        else:
            await interaction.response.send_message("Could not reject user (not found).", ephemeral=True)
        self.disable_all_items()
        await interaction.message.edit(view=self)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    try:
        unverified_role = member.guild.get_role(UNVERIFIED_ROLE)
        await member.add_roles(unverified_role) #added this line
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
    if isinstance(message.channel, discord.DMChannel) and not message.author.bot:
        # Get the guild and member object
        guild = bot.get_guild(YOUR_GUILD_ID)  # Replace with your server's ID
        if guild:
            member = guild.get_member(message.author.id)
            if member:
                verified_role = guild.get_role(VERIFIED_ROLE_ID)
                if verified_role in member.roles:
                    await message.channel.send(
                        "You are already verified! If you have questions, please contact a moderator."
                    )
                    return  # Stop processing further

        # If not verified, continue as before
        if message.attachments:
            mod_channel = bot.get_channel(MOD_CHANNEL_ID)
            if mod_channel:
                files = [await a.to_file() for a in message.attachments]
                embed = discord.Embed(
                    title="Verification Request",
                    description=f"From: {message.author} ({message.author.id})",
                    color=discord.Color.blue()
                )
                # embed.set_image(url=message.attachments[0].url)
                view = VerificationView(user_id=message.author.id)
                await mod_channel.send(
                    content="<@480410162365071360> New verification request!",
                    embed=embed,
                    files=files,
                    view=view
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

bot.run(TOKEN)