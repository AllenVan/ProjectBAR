import asyncio
import discord
import random

from discord.ext import commands
from discord.ui import Select, View


class Traversal(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.__reset_floor()

	def __reset_floor(self):
		self.floor = self.__generate_floor()
		self.current_room = self.floor[7]

	def __generate_floor(self):
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
					if self.client.job == None:
						icon = self.client._map["player"]["icon"]
					else:
						icon = self.client.job["icon"]
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
	async def move(self, ctx, direction):
		if self.client.job == None:
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
			if self.current_room.type == "enemy" and not self.current_room.defeated:
				await ctx.invoke(self.client.get_command("battle"))

				while self.client.enemy:
					await asyncio.sleep(1)

				if self.client.job == None: # Player died
					# TODO: invoke reset player
					self.floor = self.__generate_floor()
					self.current_room = self.floor[7]
					return
				else:
					self.current_room.defeated = True
			elif self.current_room.type == "exit":
				async def callback(interaction):
					choice = select_menu.values[0]
					if choice == "Yes":
						# TODO: invoke reset player
						await interaction.response.send_message("You have beaten the dungeon", ephemeral=False)
						self.__reset_floor()
					else:
						await interaction.response.send_message("Your journey continues", ephemeral=False)
					return

				embed_message=discord.Embed(title="You have found the exit. Would you like to continue?")
				select_menu = Select(options=[])
				for item in ["Yes", "No"]:
					select_menu.append_option(discord.SelectOption(
						label=item
					))
				select_menu.callback = callback
				view = View()
				view.add_item(select_menu)
				await ctx.send(embed=embed_message, view=view, ephemeral=False)

			await ctx.invoke(self.client.get_command("map"))

	@commands.command(aliases=["m"])
	async def map(self, ctx):
		if self.client.job == None:
			await ctx.send("You have not selected a job. Use `.start` command", ephemeral=True)
		else:
			self.current_room.set_icon() # Update default player icon after job selection

			embed_message = discord.Embed(
				title="Map",
				color=discord.Color.dark_red()
			)

			map_string = f"""
			{self.floor[0].icon} {self.floor[1].icon} {self.floor[2].icon}
			{self.floor[3].icon} {self.floor[4].icon} {self.floor[5].icon}
			{self.floor[6].icon} {self.floor[7].icon} {self.floor[8].icon}
			"""

			embed_message.add_field(name="", value=map_string, inline=False)
			await ctx.send(embed=embed_message, ephemeral=False)


async def setup(client):
	await client.add_cog(Traversal(client))
