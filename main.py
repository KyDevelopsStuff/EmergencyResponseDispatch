import sqlite3
import asyncio
import discord
from discord import app_commands
from discord.ext import commands

#### BOT CONFIG
dispatch_channelID = "1252821712089911306" # Put the channel you want calls fowarded to.
token = "MTI0MjMyMzA5MjM2NjI5NTA2MA.GIh5KV.sj0OkYmpBDk1qhtqi6V38hvvtCzkfgliDfIgWg" # Bot Token Here. This token is useless as it just belongs to an old bot of mine in a useless server.


# Initialize the discord bot
con = sqlite3.connect("data.db")
cur = con.cursor()
bot = commands.Bot(intents=discord.Intents.all(), command_prefix='cad!')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.tree.sync()

# Misc
callouts = cur.execute("SELECT * FROM call").fetchall()
calloutsstring = str(callouts)
calloutsformatted = ''
for char in calloutsstring:
        if char != '(' and char != ')' and char != '[' and char != ']' and char != "'":
            calloutsformatted += char


     


#### NON SLASH COMMANDS
@bot.command()
async def botping(ctx):
    botlatencyrounded = round(bot.latency, 4)
    await ctx.send(f"Pong! {botlatencyrounded}ms")

@bot.command()
async def activecallouts(ctx):
    emb = discord.Embed(title="ACTIVE CALLOUTS", color=0xaa3a3a)
    emb.description = f"""All the active callouts will be displayed below. Please remember callouts get deleted after 30 minutes.

                          Callouts are displayed in the format of Postal Code, Code, Caller, Emergency Service Required.
                          ** CALLOUTS: **
                          {calloutsformatted}"""
    emb.set_author(name="")
    emb.set_image(url="")

    await ctx.send(embed=emb)

#
     

#### BOT COMMANDS

# Ping
@bot.tree.command(name="ping", description="Ping the discord bot to see its latency.")
async def ping(interaction: discord.Interaction):
    botlatencyrounded = round(bot.latency, 4)
    await interaction.response.send_message(f"Pong! {botlatencyrounded}ms")

# View Callouts
@bot.tree.command(name="active_callouts", description="View all active callouts.")
async def active_callouts(interaction: discord.Interaction):
    emb = discord.Embed(title="ACTIVE CALLOUTS", color=0xaa3a3a)
    emb.description = f"""All the active callouts will be displayed below. Please remember callouts get deleted after 30 minutes.
                        Callouts are displayed in the format of Postal Code, Code, and Emergency Service Required.
                        **CALLOUTS:**
                          {calloutsformatted}"""
    emb.set_author(name="")
    emb.set_image(url="")

    await interaction.response.send_message(embed=emb)

# Create Callout
@bot.tree.command(name="createcallout", description="Create a emergency service callout.")
@app_commands.describe(postal = "The postal code for the callout.")
@app_commands.describe(code = "The code / urgency of the call.")
@app_commands.choices(code = [
    app_commands.Choice(name="Code 2", value="2"),
    app_commands.Choice(name="Code 3", value="3"),
    app_commands.Choice(name="Code 4", value="4"),
    app_commands.Choice(name="Code 5", value="5"),
    app_commands.Choice(name="Code 9", value="9"),
])
@app_commands.describe(es_required = "The Emergency Service required.")
@app_commands.choices(es_required = [
    app_commands.Choice(name="Los Angeles County Sheriff", value="LASD"),
    app_commands.Choice(name="Los Angeles Police Dept.", value="LAPD"),
    app_commands.Choice(name="Los Angeles Fire Dept.", value="LAFD"),
    app_commands.Choice(name="California Highway Patrol", value="CHP"),
    app_commands.Choice(name="CalTrans", value="CalTrans"),
])
async def createcallout(interaction: discord.Interaction, postal: str, code: str, es_required: str):
    cur.execute(f"INSERT INTO call VALUES({postal}, {code}, {es_required})")
    con.commit()
    print(f"Callout created. **POSTAL:** {postal}, **CODE:** {code}, **EMERGENCY SERVICE REQUIRED:** {es_required}")
    emb = discord.Embed(title="Callout sent", color=0xaa3a3a)
    emb.description = f"""Callout created sucessfully. All callout info displayed below. 
                          Callout will be automatically deleted in 20 minutes.
                          
                          **POSTAL CODE:** {postal}
                          **CODE:** {code}
                          **EMERGENCY SERVICE REQUIRED:** {es_required}"""
    emb.set_author(name="")
    emb.set_image(url="")

    await interaction.response.send_message(embed=emb)

#### RUN BOT
bot.run(token=token)
