import discord
from discord.ext import commands
from discord.ui import Select, View


class Player(commands.Cog):
	
	def __init__(self, client):
		self.client = client
		self.client.job = None
		self.client.level = 1
		self.client.hp = 100

	@commands.Cog.listener()
	async def on_ready(self):
		print("Loading cog: select.py")
	
	@commands.command()  # .start command
	async def start(self, ctx):
		select_menu = Select(options=[])  # create an instance of the Select() class with an empty list of options

		# for loop is used to iterate through json file and create options for dropdown menu for Select() instance
		for item in self.client._jobs.values():
			select_menu.append_option(discord.SelectOption(
				label=item['name'],
				emoji=item['icon'],
				description=item['description']
			))

		# the function called when the user is done selecting options
		async def callback(interaction):  
			# select_menu.values is simply an array of selections made by the user
			# user can only choose 1 option so we use the first and only value in the array
			self.client.job = self.client._jobs[select_menu.values[0].lower()]  # job_list is used here as a quick way to reference index for "jobs" dictionary value
			await interaction.response.send_message(f"You are now: {select_menu.values[0]}")
			

		select_menu.callback = callback  # define Select() instance callback as the above callback function
		view = View()  # create an instance of View() in order to send a message
		view.add_item(select_menu)  # add Select() instance to View() instance

		embed_message = discord.Embed(
			title="Select Job",
			color=discord.Color.light_gray()
		)
		
		embed_message.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
		await ctx.send(embed=embed_message, view=view, ephemeral=True)

	@commands.command()
	async def player(self, ctx):
		if self.client.job == None:
			await ctx.send("You have not selected a job. Use `.start` command")
		else:
			embed_message = discord.Embed(
				title="Player Info",
				color=discord.Color.dark_blue()
			)
			embed_message.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)

			weapon = self.client.job["starting_inventory"]["weapon"].capitalize()

			embed_message.add_field(name="Job", value=f"{self.client.job['name']}", inline=False)
			embed_message.add_field(name="Weapon", value=weapon, inline=False)
			await ctx.send(embed=embed_message, ephemeral=True)


async def setup(client):
	await client.add_cog(Player(client))
