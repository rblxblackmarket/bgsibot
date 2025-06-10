import discord
from discord.ext import commands
from discord import app_commands
import os

# Required Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot Setup
bot = commands.Bot(command_prefix="!", intents=intents)
trade_id_file = "trade_id.txt"
TRADE_LOG_CHANNEL_ID = 1381178922036887655  # ⬅️ Replace with your log channel ID
ALLOWED_ROLES = ["Owner", "Admins"]


# Load Trade ID from file
def load_trade_id():
    if os.path.exists(trade_id_file):
        with open(trade_id_file, "r") as f:
            return int(f.read())
    return 1


# Save Trade ID to file
def save_trade_id(value):
    with open(trade_id_file, "w") as f:
        f.write(str(value))


# Initialize trade ID
trade_id = load_trade_id()


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot is online as {bot.user} — Slash commands synced.")


@bot.tree.command(name="deal", description="Log a completed trade.")
@app_commands.describe(sender="User who sent the item or payment",
                       receiver="User who received the item or payment",
                       item="What was traded")
async def deal(interaction: discord.Interaction, sender: discord.Member,
               receiver: discord.Member, item: str):
    global trade_id

    # Check role permissions
    if not any(role.name in ALLOWED_ROLES for role in interaction.user.roles):
        await interaction.response.send_message(
            "❌ You don’t have permission to use this command.", ephemeral=True)
        return

    trade_channel = bot.get_channel(TRADE_LOG_CHANNEL_ID)
    if trade_channel is None:
        await interaction.response.send_message(
            "❌ Trade log channel not found.", ephemeral=True)
        return

    embed = discord.Embed(title="✅ Trade Completed", color=0x00ff00)
    embed.add_field(name="Sender", value=sender.mention, inline=True)
    embed.add_field(name="Receiver", value=receiver.mention, inline=True)
    embed.add_field(name="Item", value=item, inline=False)
    embed.set_footer(text=f"RobloxBlackMarket • Trade ID #{trade_id:03d}")

    await trade_channel.send(embed=embed)
    await interaction.response.send_message("✅ Trade logged successfully.",
                                            ephemeral=True)

    trade_id += 1
    save_trade_id(trade_id)


bot.run(
    "MTM4MTY0NzIyNTAyOTEzNjQ3NA.Gyo-02.mIa70kwAHBV5QXsp7mT_MLu66fFIyX2CVmXllw")
