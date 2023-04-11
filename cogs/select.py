import discord
from discord.ext import commands


class Select(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.class_name = None

	@commands.Cog.listener()
	async def on_ready(self):
		print("Loading cog: select.py")
	
	@commands.command()
	async def start(self, ctx):
		class_list = []
		for class_name, class_info in self.client._classes.items():
			class_list.append(f"{class_info['icon']} {class_name.capitalize()}")

		embed_message = discord.Embed(
			title="Select Class",
			description="\n\n".join(class_list),
			color=discord.Color.light_gray()
		)
		
		embed_message.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
		await ctx.send(embed=embed_message, view=SelectClass(self), ephemeral=True)

	@commands.command()
	async def player(self, ctx):
		if self.class_name == None:
			await ctx.send("You have not selected a class. Use `.start` command")
		else:
			embed_message = discord.Embed(
				title="Player Info",
				color=discord.Color.dark_blue()
			)
			embed_message.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)

			weapon = self.class_info["starting_inventory"]["weapon"].capitalize()

			embed_message.add_field(name="Class", value=f"{self.class_info['icon']} {self.class_name.capitalize()}", inline=False)
			embed_message.add_field(name="Weapon", value=weapon, inline=False)
			await ctx.send(embed=embed_message, ephemeral=True)


class SelectClass(discord.ui.View):
	def __init__(self, user: Select):
		super().__init__()

		self.user = user

	# TODO: Dynamically define buttons
	@discord.ui.button(label="🏹", style=discord.ButtonStyle.blurple)
	async def archer_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		self.user.class_name =  "archer"
		self.user.class_info = self.user.client._classes[self.user.class_name]
		await interaction.response.send_message(f"Poof you are {self.user.class_name}", ephemeral=True)

	@discord.ui.button(label="🧙", style=discord.ButtonStyle.blurple)
	async def mage_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		self.user.class_name = "mage"
		self.user.class_info = self.user.client._classes[self.user.class_name]
		await interaction.response.send_message(f"Poof you are {self.user.class_name}", ephemeral=True)

	@discord.ui.button(label="🛡️", style=discord.ButtonStyle.blurple)
	async def knight_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		self.user.class_name =  "knight"
		self.user.class_info = self.user.client._classes[self.user.class_name]
		await interaction.response.send_message(f"Poof you are {self.user.class_name}", ephemeral=True)


async def setup(client):
	await client.add_cog(Select(client))
