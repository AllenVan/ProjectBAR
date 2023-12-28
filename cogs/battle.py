import discord
from discord.ext import commands
from discord.ui import Select, View
from skills import CombatSkills
import random

def battle_end(ctx, enemy_killed):
		if enemy_killed:
			temp_message=discord.Embed(title=f'The enemy has been slain!', color=discord.Color.green())
			temp_message.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
			temp_message.set_footer(text=f"You live to fight another day...")
		else:
			temp_message=discord.Embed(title=f"You Died!", color=discord.Color.red())
			temp_message.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
			temp_message.set_footer(text=f"Better luck next time...")
		return temp_message

class BattleSystem(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.client.enemy = None
		self.player_message = None
		self.enemy_message = None

	def spawn(self):
		self.client.enemy = random.choice(self.client._spawns['mobs']).copy()
		self.combat_skills = CombatSkills()

	@commands.Cog.listener()
	async def on_ready(self):
		print("Loading cog: battle.py")

	@commands.command(description="start a fight")
	async def battle(self, ctx):
		if self.client.player == None:
			await ctx.send("You have not selected a job. Use `.start` command")
		else:
			async def callback(interaction):
				self.player_message, e_damage = getattr(self.combat_skills, select_menu.values[0])()  # calls a function in skills.py class with the same name
				self.enemy_message, p_damage = getattr(self.combat_skills, random.choice(self.client.enemy['skills']))()
				
				if self.client.enemy["HP"] - e_damage <= 0:
					embed_message=battle_end(ctx, True)
					self.client.enemy = None
					view.remove_item(select_menu)
					await interaction.response.send_message(embed=embed_message, view=view, ephemeral=False)
				elif self.client.player["HP"] - p_damage <= 0:
					embed_message=battle_end(ctx, False)
					self.client.player = None
					self.client.enemy = None
					view.remove_item(select_menu)
					await interaction.response.send_message(embed=embed_message, view=view, ephemeral=False)
				else:
					self.client.enemy["HP"] -= max(e_damage + self.combat_skills.damage_modifiers[0], 0)
					self.client.player["HP"] -= max(p_damage + self.combat_skills.damage_modifiers[1], 0)
					self.combat_skills.damage_modifiers = [0,0]
					await ctx.invoke(self.client.get_command("battle"))
					await interaction.response.defer() # "closes" the current embed interaction now that reinvoked is called
					
			if self.client.enemy:
				embed_message=discord.Embed(title=f'The {self.client.enemy["name"]} did not hear no bell.', color=discord.Color.light_gray())
				embed_message.add_field(name="Player", value=self.player_message, inline=True)
				embed_message.add_field(name="Enemy", value=self.enemy_message, inline=True)
			else:
				self.spawn()
				embed_message=discord.Embed(title=f'The {self.client.enemy["name"]} ambushes you!', color=discord.Color.light_gray())
				embed_message.set_image(url=self.client.enemy['image'])

			embed_message.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
			embed_message.set_footer(text=f'What will you do? Distance is {self.combat_skills.distance}. Your HP is {self.client.player["HP"]}. Enemy HP is {self.client.enemy["HP"]}.')

			select_menu = Select(options=[discord.SelectOption(label=item) for item in self.client.player["skills"].values()])

			select_menu.callback = callback
			view = View()
			view.add_item(select_menu)
			await ctx.send(embed=embed_message, view=view, ephemeral=False)

async def setup(client):
	await client.add_cog(BattleSystem(client))
