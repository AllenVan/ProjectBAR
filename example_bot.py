# This example requires the 'message_content' intent.

import discord
from discord import app_commands


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

@tree.command(name = "introduce", description = "My first application Command", guild=discord.Object(id=688838108749365350)) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction):
    await interaction.response.send_message("Hello!")

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=688838108749365350))
    print("Ready!")


#### Create the initial embed object ####
embed=discord.Embed(title="Example", url="https://i.redd.it/4rb49b4ot6ra1.png", description="Sample Embed", color=0x109319)

# Add author, thumbnail, fields, and footer to the embed
embed.set_author(name="RaulCard", url="https://github.com/RaulCard", icon_url="https://avatars.githubusercontent.com/u/31727722?v=4")

embed.set_thumbnail(url="https://i.imgflip.com/74n62t.jpg")

embed.add_field(name="Field 1 Title", value="This is the value for field 1. This is NOT an inline field.", inline=False)
embed.add_field(name="Field 2 Title", value="It is inline with Field 3", inline=True)
embed.add_field(name="Field 3 Title", value="It is inline with Field 2", inline=True)

embed.set_footer(text="This is the footer. It contains text at the bottom of the embed")


@client.event
async def on_message(message):
    if message.content.startswith('!embed'):
        await message.channel.send(embed=embed)


client.run('')
