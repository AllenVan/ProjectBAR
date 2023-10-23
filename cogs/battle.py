import discord
from discord.ext import commands
from discord.ui import Select, View
import random


class battleSystem(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.client.enemy = None
	
	def spawn(self):
		self.client.enemy = random.choice(self.client._spawns['mobs']).copy()

	@commands.Cog.listener()
	async def on_ready(self):
		print("Loading cog: battle.py")

	@commands.command()
	async def battle(self, ctx):
		if self.client.player == None:
			await ctx.send("You have not selected a job. Use `.start` command")

		else:
			async def callback(interaction):
				# select_menu.values is simply an array of selections made by the user
				# user can only choose 1 option so we use the first and only value in the array
				
				view = View()
				p_message, e_damage = getattr(self.client.combat_skills, select_menu.values[0])()  # calls a function in skills.py class with the same name
				e_message, p_damage = getattr(self.client.combat_skills, random.choice(self.client.enemy['skills']))()
				
				if self.client.enemy["HP"] - e_damage <= 0:
					embed_message=discord.Embed(title=f'The {self.client.enemy["name"]} is slain!', color=discord.Color.green())
					footer_text=f'You live to fight another day...'
					self.client.enemy = None
				elif self.client.player["HP"] - p_damage <= 0:
					embed_message=discord.Embed(title=f"You Died!", color=discord.Color.red())
					footer_text=f"Better luck next time..."
					self.client.player = None
					self.client.enemy = None
				else:
					self.client.player["HP"] -= p_damage
					self.client.enemy["HP"] -= e_damage
					embed_message=discord.Embed(title=f"Battle!", color=discord.Color.dark_gray())
					embed_message.add_field(name="Player", value=p_message, inline=True)
					embed_message.add_field(name="Enemy", value=e_message, inline=True)
					footer_text=f'What will you do? Distance is {self.client.combat_skills.distance}. Your HP is {self.client.player["HP"]}. Enemy HP is {self.client.enemy["HP"]}.'
					select_menu.callback = callback
					view.add_item(select_menu)
				
				embed_message.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
				embed_message.set_footer(text=footer_text)
				await interaction.response.send_message(embed=embed_message, view=view, ephemeral=False)

			if self.client.enemy:
				embed_message=discord.Embed(title=f'The {self.client.enemy["name"]} did not hear no bell.', color=discord.Color.light_gray())
			else:
				self.spawn()
				embed_message=discord.Embed(title=f'The {self.client.enemy["name"]} ambushes you!', color=discord.Color.light_gray())

			embed_message.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
			embed_message.set_image(url=self.client.enemy['image'])
			embed_message.set_footer(text=f'What will you do? Distance is {self.client.combat_skills.distance}. Your HP is {self.client.player["HP"]}. Enemy HP is {self.client.enemy["HP"]}.')

			select_menu = Select(options=[])
			for item in self.client.player["skills"].values():
				select_menu.append_option(discord.SelectOption(
					label=item
				))

			select_menu.callback = callback
			view = View()
			view.add_item(select_menu)
			await ctx.send(embed=embed_message, view=view, ephemeral=False)

async def setup(client):
	await client.add_cog(battleSystem(client))
