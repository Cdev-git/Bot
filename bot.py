import discord
from discord.ext import commands
import asyncio
import random
import datetime
import io
import os
import time
from discord.ext import commands

OWNER_ID = 1243374094385283085
Website_latest = "https://github.com/sigmaclient123-droid/LIQUID.CLIENT/releases/download/v1.2.6/liquid.client.dll"
Website = "https://github.com/sigmaclient123-droid/LIQUID.CLIENT/releases/latest"
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
PREFIX = "-"
ALLOWED_IDS = [OWNER_ID, 1256555669985824799, 815988562464997397, 1407049985907884123, 1432590680831688759, 1354194646661599282]

bot = commands.Bot(command_prefix=PREFIX, intents=intents, owner_id=OWNER_ID)

def is_allowed():
    async def predicate(ctx):
        return ctx.author.id in ALLOWED_IDS
    return commands.check(predicate)

def parse_duration(duration: str) -> int:
    unit = duration[-1].lower()
    if unit == "s":
        mult = 1
    elif unit == "m":
        mult = 60
    elif unit == "h":
        mult = 3600
    elif unit == "d":
        mult = 86400
    else:
        raise ValueError("Oops, use s, m, h, or d at the end (like 1h or 30m)")
    try:
        return int(duration[:-1]) * mult
    except ValueError:
        raise ValueError("That time format isn't right")

@bot.event
async def on_ready():
    print(f"Bot running allowed ids' are {ALLOWED_IDS}")

# BAN
@bot.command()
@is_allowed()
async def ban(ctx, member: discord.Member, *, reason: str = "no reason given"):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}. Reason: {reason}. They're gone now")



# meme2
@bot.command()
@is_allowed()
async def meme2(ctx):
    Video = "https://youtu.be/yLPSZE8hwgw"
    await ctx.message.delete()
    await ctx.send(f"[Meme]({Video})")

# horror
@bot.command()
async def horror(ctx):
    Person = ctx.author.mention
    Pic = "What.png"
    ram = "https://www.amazon.com/G-SKILL-Trident-CL36-36-36-96-Desktop-Computer/dp/B0DN3WFS52/ref=sr_1_13?sr=8-13"
    await ctx.message.delete()
    await ctx.send(f"[Horror]({ram})", delete_after=50)

    
    file = discord.File(Pic)
    await ctx.send(file=file)
    await ctx.send(f"Sent by {Person}")

# Installer
#@bot.command()
#async def installer(ctx):
#    Person = ctx.author.mention
 #   Installer = "Installer.bat"
 #   file = discord.File(Installer)
#    await ctx.message.delete()

    
#    await ctx.send(file=file, delete_after=30)
 #   await ctx.send(f"Sent by {Person}", delete_after=30)


# TEMPBAN
@bot.command()
@is_allowed()
async def tempban(ctx, member: discord.Member, duration: str, *, reason: str = "no reason given"):
    try:
        seconds = parse_duration(duration)
    except ValueError as e:
        await ctx.send(f"Oops, {e}")
        return
    await member.ban(reason=reason)
    await ctx.send(f"Temp-banned {member.mention} for {duration}. Reason: {reason}.")
    await asyncio.sleep(seconds)
    await ctx.guild.unban(member)
    await ctx.send(f"{member.mention} is back! Auto-unbanned.")

# KICK
@bot.command()
@is_allowed()
async def kick(ctx, member: discord.Member, *, reason: str = "no reason given"):
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.mention} out. Reason: {reason} 👟")

# Show token (commented)
##@bot.command()
##@is_allowed()
##async def Bot_token(ctx):
    ##await ctx.send(f"{TOKEN}")
# allow reactions
@bot.command()
@is_allowed()
async def Allow_reactions(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    await channel.set_permissions(ctx.guild.default_role, add_reactions=True)
    await ctx.send(f"{channel.mention}Reactions allowed!")

@bot.command()
@is_allowed()
async def Disable_reactions(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    await channel.set_permissions(ctx.guild.default_role, add_reactions=False)
    await ctx.send(f"{channel.mention}No reactions allowed!")

# Download
#@bot.command()
#async def download(ctx):
#    Person = ctx.author.mention
#    await ctx.message.delete()
#    await ctx.send(f"{Person} Install here [Download]({Website})", delete_after=10)
# straight download
#@bot.command()
#async def downloadlink(ctx):
 #   Person = ctx.author.mention
 #   await ctx.message.delete()
  #  await ctx.send(f"{Person} Click to install the dll [Download]({Website_latest})", delete_after=10)

# MUTE
@bot.command()
@is_allowed()
async def mute(ctx, member: discord.Member, duration: str, *, reason: str = "no reason given"):
    try:
        seconds = parse_duration(duration)
        await member.edit(mute=True, reason=reason)
        await ctx.send(f"Voice muted {member.mention} for {duration}. They can't speak in VC now 😶")
        await asyncio.sleep(seconds)
        await member.edit(mute=False)
        await ctx.send(f"{member.mention} can speak in VC again! Voice unmuted 🎙️")
    except ValueError as e:
        await ctx.send(f"Oops, {e}")
    except Exception:
        await ctx.send("Couldn't voice mute them (I probably need 'Mute Members' permission).")

# UNMUTE (voice)
@bot.command()
@is_allowed()
async def unmute(ctx, member: discord.Member):
    try:
        await member.edit(mute=False)
        await ctx.send(f"{member.mention} can talk in voice again! Unmuted 🎉")
    except Exception:
        await ctx.send("Couldn't unmute them (check my perms).")

# LOCK
@bot.command()
@is_allowed()
async def lock(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    await channel.set_permissions(ctx.guild.default_role, send_messages=False, add_reactions=False)
    await ctx.send(f"🔒 Locked down {channel.mention}. No chatting allowed!")

# UNLOCK
@bot.command()
@is_allowed()
async def unlock(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    await channel.set_permissions(ctx.guild.default_role, send_messages=True, add_reactions=True)
    await ctx.send(f"🔓 Unlocked {channel.mention}. Chat is back on!")

# SLOWMODE
@bot.command(aliases=['sm'])
@is_allowed()
async def slowmode(ctx, seconds: int, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    await channel.edit(slowmode_delay=seconds)
    if seconds == 0:
        await ctx.send(f"Slowmode disabled in {channel.mention} - chat as fast as you want! 🚀")
    else:
        await ctx.send(f"Slowmode set to **{seconds}s** in {channel.mention}. Take it easy 😌")

# PURGE
@bot.command()
@is_allowed()
async def purge(ctx, amount: int):
    Person = ctx.author.mention
    if amount < 1:
        await ctx.message.delete()
        await ctx.send(f"{Person}, amount has to be at least 1!", delete_after=2)
        return
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Cleaned up {amount} messages.", delete_after=2)

# SAY
@bot.command()
@is_allowed()
async def say(ctx, *, text: str):
    Person = ctx.author.mention
    if text:
        await ctx.message.delete()
        await ctx.send(text)
    else:
        await ctx.send(f"{Person} What do you want me to say?")
# meme
Meme_path = "7ks8tf.webp"
@bot.command()
async def meme(ctx):
    Person = ctx.author.mention
    await ctx.message.delete()
    file = discord.File(Meme_path)
    await ctx.send(file=file)
    await ctx.send(f"Sent by {Person}")

# GIVEAWAY
@bot.command()
@is_allowed()
async def giveaway(ctx, *, content: str):
    ctx.message.delete()
    parts = [p.strip() for p in content.split('&') if p.strip()]
    if len(parts) < 2:
        await ctx.send("Usage: `-giveaway 30m & Prize name with many words here`")
        return
    duration = parts[0]
    prize = " & ".join(parts[1:])
    try:
        seconds = parse_duration(duration)
    except ValueError as e:
        await ctx.send(f"Oops, {e}")
        return
    embed = discord.Embed(
        title="🎉 GIVEAWAY TIME! 🎉",
        description=f"**Prize:** {prize}\nReact with 🎉 to enter!\nEnds in {duration}",
        color=0x00ff00
    )
    embed.set_footer(text=f"Hosted by {ctx.author}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")
    await asyncio.sleep(seconds)
    msg = await ctx.channel.fetch_message(msg.id)
    reaction = discord.utils.get(msg.reactions, emoji="🎉")
    if reaction:
        users = [user async for user in reaction.users() if not user.bot]
        if users:
            winner = random.choice(users)
            await ctx.send(f"🎉 Congrats {winner.mention}! You won **{prize}**!")
        else:
            await ctx.send("Nobody entered the giveaway this time.")
    else:
        await ctx.send("Giveaway ended with no reactions.")

# POLL
@bot.command()
@is_allowed()
async def poll(ctx, *, content: str):
    await ctx.message.delete()
    parts = [p.strip() for p in content.split('&') if p.strip()]
    if len(parts) < 3 or len(parts) > 11:
        await ctx.send("Usage: `-poll Question with words? & Option one & Option two & Option three` (2-10 options)")
        return
    question = parts[0]
    options = parts[1:]
    if len(options) < 2 or len(options) > 10:
        await ctx.send("A poll needs between 2 and 10 options!")
        return
    emojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
    embed = discord.Embed(title="📊 Quick Poll", description=question, color=0x00ff00)
    for i, option in enumerate(options):
        embed.add_field(name=emojis[i], value=option, inline=False)
    msg = await ctx.send(embed=embed)
    for i in range(len(options)):
        await msg.add_reaction(emojis[i])
    await ctx.send("Poll is live! React to vote.")

if __name__ == "__main__":
    if not TOKEN:
        print("ERROR: Set TOKEN environment variable in Railway!")
        exit(1)
    while True:
        try:
            print("Starting bot...")
            bot.run(TOKEN)
            break
        except discord.errors.HTTPException as e:
            if "429" in str(e) or "Too Many Requests" in str(e) or "1015" in str(e):
                print("Cloudflare rate limit hit → waiting 90 seconds...")
                time.sleep(90)
            else:
                print(f"Discord error: {e}")
                time.sleep(10)
        except Exception as e:
            print(f"Unexpected crash: {e}")
            time.sleep(10)
