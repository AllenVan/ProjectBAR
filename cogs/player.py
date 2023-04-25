import discord
from discord.ext import commands


class Select(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.job = None

	@commands.Cog.listener()
	async def on_ready(self):
		print("Loading cog: select.py")
	
	@commands.command()
	async def start(self, ctx):
		job_list = []
		for job_name, job_info in self.client._jobs.items():
			job_list.append(f"{job_info['icon']} {job_name.capitalize()}")

		embed_message = discord.Embed(
			title="Select Job",
			description="\n\n".join(job_list),
			color=discord.Color.light_gray()
		)
		
		embed_message.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
		await ctx.send(embed=embed_message, view=SelectJob(self), ephemeral=True)

	@commands.command()
	async def player(self, ctx):
		if self.job == None:
			await ctx.send("You have not selected a job. Use `.start` command")
		else:
			embed_message = discord.Embed(
				title="Player Info",
				color=discord.Color.dark_blue()
			)
			embed_message.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)

			weapon = self.job_info["starting_inventory"]["weapon"].capitalize()

			embed_message.add_field(name="Job", value=f"{self.job_info['icon']} {self.job.capitalize()}", inline=False)
			embed_message.add_field(name="Weapon", value=weapon, inline=False)
			await ctx.send(embed=embed_message, ephemeral=True)


class SelectJob(discord.ui.View):
	def __init__(self, user: Select):
		super().__init__()

		self.user = user

	def set_job(self, job_name):
		self.user.job = job_name
		self.user.job_info = self.user.client._jobs[self.user.job]

	# TODO: Dynamically define buttons
	@discord.ui.button(label="🏹", style=discord.ButtonStyle.blurple)
	async def archer_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		self.set_job(job_name="archer")
		await interaction.response.send_message(f"Poof you are {self.user.job}", ephemeral=True)

	@discord.ui.button(label="🧙", style=discord.ButtonStyle.blurple)
	async def mage_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		self.set_job(job_name="mage")
		await interaction.response.send_message(f"Poof you are {self.user.job}", ephemeral=True)

	@discord.ui.button(label="🛡️", style=discord.ButtonStyle.blurple)
	async def knight_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		self.set_job(job_name="knight")
		await interaction.response.send_message(f"Poof you are {self.user.job}", ephemeral=True)


async def setup(client):
	await client.add_cog(Select(client))
