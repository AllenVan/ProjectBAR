import asyncio
import discord
import json
import logging
import os
import pathlib

from discord.ext import commands

# TODO: Add logging to class
logging.basicConfig(level=logging.INFO)


class BAR(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open("resources/jobs.json", encoding="utf8") as file:
            self._jobs = json.loads(file.read())

        with open("resources/spawns.json", encoding="utf8") as file:
            self._spawns = json.loads(file.read())  

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == client.user:
            return

        print(f'Message from {message.author}: {message.content}')
        await self.process_commands(message) # This allows the bot to process commands

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")


# Client Setup
intents = discord.Intents.all()
intents.message_content = True
client = BAR(command_prefix='.', intents=intents)

async def main():
    # TODO: Remove at the end of development
    credentials_file_path = pathlib.Path("credentials", "token.json")
    with open(credentials_file_path) as cred_file:
        token = json.loads(cred_file.read())["token"]

    async with client:
        await client.start(token) 

asyncio.run(main())
