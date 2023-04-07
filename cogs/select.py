from discord.ext import commands


class Select(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.player_class = None

	@commands.Cog.listener()
	async def on_ready(self):
		print("Loading cog: select.py")
	
	@commands.command()
	async def start(self, ctx):
		await ctx.send("Select Class")

async def setup(client):
	await client.add_cog(Select(client))
