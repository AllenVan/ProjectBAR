import discord
from discord.ext import commands


class Select(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.user_class = None

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
			color=discord.Color.light_gray())
		
		embed_message.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
		await ctx.send(embed=embed_message, view=SelectClass(self), ephemeral=True)

	@commands.command()
	async def user(self, ctx):
		if self.user_class == None:
			message = "You have not selected a class"
		else:
			message = f"You are {self.user_class}"
		await ctx.send(message)


class SelectClass(discord.ui.View):
	def __init__(self, user: Select):
		super().__init__()

		self.user = user

	# TODO: Dynamically define buttons
	@discord.ui.button(label="🏹", style=discord.ButtonStyle.blurple)
	async def archer_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		self.user.user_class =  "archer"
		await interaction.response.send_message(f"Poof you are {self.user.user_class}", ephemeral=True)

	@discord.ui.button(label="🧙", style=discord.ButtonStyle.blurple)
	async def mage_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		self.user.user_class = "mage"
		await interaction.response.send_message(f"Poof you are {self.user.user_class}", ephemeral=True)

	@discord.ui.button(label="🛡️", style=discord.ButtonStyle.blurple)
	async def knight_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		self.user.user_class =  "knight"
		await interaction.response.send_message(f"Poof you are {self.user.user_class}", ephemeral=True)


async def setup(client):
	await client.add_cog(Select(client))
