import asyncio
import discord
import random

from discord.ext import commands
from discord.ui import Select, View

MAX_FLOORS = 5


class Traversal(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.last_map_ctx = None
		self.last_exit_ctx = None

	@commands.Cog.listener()
	async def on_ready(self):
		print("Loading cog: traversal.py")

	@commands.Cog.listener()
	async def on_job_selected(self):
		self._reset_dungeon()
		await self.client.start_ctx.invoke(self.client.get_command("map"))

	@commands.Cog.listener()
	async def on_interaction(self, interaction): # Handle button presses
		id = interaction.data["custom_id"]

		if id in ("up", "down", "left", "right"): # Direction Buttons
			await self.last_map_ctx.invoke(self.client.get_command("move"), direction=id)
		elif id in ("yes_exit", "no_exit"): # Floor Exit
			if id == "yes_exit":
				self.floor_count -= 1

				if self.floor_count == 0:
					await interaction.response.send_message("You have beaten the dungeon", ephemeral=False)
					self._reset_dungeon()
					self.client.dispatch("dungeon_beat")
					return
				else:
					await interaction.response.send_message("You descend further into darkness", ephemeral=False)
					self.floor = self._generate_floor()
					self.current_room = self.floor[7]
			elif id == "no_exit":
				await interaction.response.send_message("Your journey continues", ephemeral=False)
			await self.last_exit_ctx.invoke(self.client.get_command("map"))

	def _reset_dungeon(self):
		self.floor = self._generate_floor()
		self.floor_count = MAX_FLOORS
		self.current_room = self.floor[7] # Bottom middle room

	def _generate_floor(self):
		"""
		# 0 1 2
		# 3 4 5
		# 6 7 8
		"""
		class Room():
			def __init__(self, directions: dict, starting_room=False, client=self.client):
				self.directions = directions
				self.client = client

				self.type = "undiscovered"
				self.defeated = False # For enemy room type
				self.discovered = starting_room
				self.player_here = starting_room
				self.icon = None
				self.set_icon()
				
			def set_icon(self):
				if self.player_here:
					if self.client.player == None:
						icon = self.client._map["player"]["icon"]
					else:
						icon = self.client.player["icon"]
				elif not self.discovered:
					icon = self.client._map["undiscovered"]["icon"]
				elif self.type in ["enemy", "treasure", "exit"]:
					if self.type == "enemy" and self.defeated:
						icon = self.client._map["defeated_enemy"]["icon"]
					else:
						icon = self.client._map[self.type]["icon"]
				else:
					icon = self.client._map["discovered"]["icon"]

				self.icon = icon

		# TODO: Dynamically create floor
		# Create floor
		floor = [
			Room(directions={"up": None, "down": 3,    "left": None, "right": 1}),
			Room(directions={"up": None, "down": 4,    "left": 0,    "right": 2}),
			Room(directions={"up": None, "down": 5,    "left": 1,    "right": None}),
			Room(directions={"up": 0,    "down": 6,    "left": None, "right": 4}),
			Room(directions={"up": 1,    "down": 7,    "left": 3,    "right": 5}),
			Room(directions={"up": 2,    "down": 8,    "left": 4,    "right": None}),
			Room(directions={"up": 3,    "down": None, "left": None, "right": 7}),
			Room(directions={"up": 4,    "down": None, "left": 6,    "right": 8}, starting_room=True),
			Room(directions={"up": 5,    "down": None, "left": 7,    "right": None})
		]

		# Populate floor
		enemy_count = 2
		treasure_count = 1
		exit_count = 1

		for room in random.sample(floor, len(floor)):
			if not room.player_here:
				if enemy_count > 0:
					room.type = "enemy"
					enemy_count -= 1
				elif treasure_count > 0:
					room.type = "treasure"
					treasure_count -= 1
				elif exit_count > 0:
					room.type = "exit"
					exit_count -= 1
				else:
					break

		return floor

	@commands.command(aliases=["mv"])
	async def move(self, ctx, direction=None):
		if self.client.player == None:
			await ctx.send("You have not selected a job. Use `.start` command", ephemeral=True)
		elif self.current_room.type == "enemy" and not self.current_room.defeated: # If player tries to move away from battle
			await ctx.send("Running is not an option", ephemeral=True)
		elif direction not in ("up", "down", "left", "right"):
			await ctx.send(f"'{direction}' is not a valid direction. Try: 'up', 'down', 'left', 'right'", ephemeral=True)
		else:
			room_index = self.floor.index(self.current_room)
			next_room_index = self.floor[room_index].directions[direction]
			
			if next_room_index == None:
				await ctx.send(f"Can't move here", ephemeral=True)
				return self.current_room
			
			# Change current room values
			self.current_room.discovered = True
			self.current_room.player_here = False
			self.current_room.set_icon()
			
			next_room = self.floor[next_room_index]
			next_room.player_here = True
			next_room.set_icon()

			self.current_room = next_room

			# Check for special room
			if self.current_room.type == "exit":
				self.last_exit_ctx = ctx # Save context of current exit for interaction listener

				embed_message=discord.Embed(title="You have found the exit. Would you like to continue?")

				class ExitButton(discord.ui.View):
					@discord.ui.button(label="Yes", custom_id="yes_exit", style=discord.ButtonStyle.green)
					async def yes_exit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
						pass # Interaction to be handled by listener

					@discord.ui.button(label="No", custom_id="no_exit", style=discord.ButtonStyle.red)
					async def no_exit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
						pass # Interaction to be handled by listener

				await ctx.send(embed=embed_message, view=ExitButton(), ephemeral=False)
			else:
				if self.current_room.type == "enemy" and not self.current_room.defeated:
					await ctx.invoke(self.client.get_command("battle"))

					while self.client.enemy:
						await asyncio.sleep(1)

					if self.client.player == None: # Player died
						self._reset_dungeon()
						return
					else:
						self.current_room.defeated = True
				elif self.current_room.type == "treasure":
					embed_message=discord.Embed(title="You found a treasure room...but it has already been looted")
					await ctx.send(embed=embed_message, ephemeral=True)

				await ctx.invoke(self.client.get_command("map"))

	@commands.command(aliases=["m"])
	async def map(self, ctx):
		if self.client.player == None:
			await ctx.send("You have not selected a job. Use `.start` command", ephemeral=True)
		else:
			self.current_room.set_icon() # Update default player icon after job selection

			embed_message = discord.Embed(
				title=f"Floor {(MAX_FLOORS + 1) - self.floor_count}",
				color=discord.Color.dark_red()
			)

			map_string = f"""
			{self.floor[0].icon} {self.floor[1].icon} {self.floor[2].icon}
			{self.floor[3].icon} {self.floor[4].icon} {self.floor[5].icon}
			{self.floor[6].icon} {self.floor[7].icon} {self.floor[8].icon}
			"""
			embed_message.add_field(name="", value=map_string, inline=False)
			self.last_map_ctx = ctx # Save context of current command for interaction listener

			class DirectionButton(discord.ui.View):
				@discord.ui.button(label="", custom_id="left", style=discord.ButtonStyle.primary, emoji="⬅️")
				async def left_button(self, interaction: discord.Interaction, button: discord.ui.Button):
					await interaction.response.defer()

				@discord.ui.button(label="", custom_id="up", style=discord.ButtonStyle.primary, emoji="⬆️")
				async def up_button(self, interaction: discord.Interaction, button: discord.ui.Button):
					await interaction.response.defer()

				@discord.ui.button(label="", custom_id="down", style=discord.ButtonStyle.primary, emoji="⬇️")
				async def down_button(self, interaction: discord.Interaction, button: discord.ui.Button):
					await interaction.response.defer()

				@discord.ui.button(label="", custom_id="right", style=discord.ButtonStyle.primary, emoji="➡️")
				async def right_button(self, interaction: discord.Interaction, button: discord.ui.Button):
					await interaction.response.defer()
			
			await ctx.send(embed=embed_message, view=DirectionButton(), ephemeral=False)

async def setup(client):
	await client.add_cog(Traversal(client))
