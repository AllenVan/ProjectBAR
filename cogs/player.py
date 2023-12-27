import discord
from discord.ext import commands
from discord.ui import Select, View


class Player(commands.Cog):
	
	def __init__(self, client):
		self.client = client
		self.client.player = None

	@commands.Cog.listener()
	async def on_ready(self):
		print("Loading cog: select.py")
	
	@commands.command(aliases=["s"])
	async def start(self, ctx, job=None):
		# Populate job selection menu
		select_menu = Select(options=[])

		# for loop is used to iterate through json file and create options for dropdown menu for Select() instance
		for item in self.client._jobs.values():
			select_menu.append_option(discord.SelectOption(
				label=item['name'],
				emoji=item['icon'],
				description=item['description']
			))

		async def callback(interaction=None, job=None):
			if job:
				if job.lower() not in self.client._jobs:
					await ctx.send("Invalid job. Use `.start` command to view all available jobs", ephemeral=True)
				else:
					self.client.player = self.client._jobs[job.lower()]
					self.client.player["level"] = 1
					await ctx.send(f'You are now: {self.client.player["name"]}')
			else:
				# user can only choose 1 option so we use the first and only value in the array
				self.client.player = self.client._jobs[select_menu.values[0].lower()].copy()
				self.client.player["level"] = 1
				await interaction.response.send_message(f"You are now: {select_menu.values[0]}")
			
		if job: # Immediately set job if user passes it in
			await callback(job=job)
		else:
			select_menu.callback = callback  # define Select() instance callback as the above callback function
			view = View()
			view.add_item(select_menu)

			embed_message = discord.Embed(
				title="Select Job",
				color=discord.Color.light_gray()
			)

			embed_message.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
			await ctx.send(embed=embed_message, view=view, ephemeral=True)

	@commands.command(aliases=["p"])
	async def player(self, ctx):
		if self.client.player == None:
			await ctx.send("You have not selected a job. Use `.start` command")
		else:
			embed_message = discord.Embed(
				title="Player Info",
				color=discord.Color.dark_blue()
			)
			embed_message.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)

			weapon = self.client.player["starting_inventory"]["weapon"].capitalize()

			embed_message.add_field(name="Job", value=f"{self.client.player['name']}", inline=False)
			embed_message.add_field(name="Weapon", value=weapon, inline=False)
			await ctx.send(embed=embed_message, ephemeral=True)


async def setup(client):
	await client.add_cog(Player(client))
