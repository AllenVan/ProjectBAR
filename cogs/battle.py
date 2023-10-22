import discord
from discord.ext import commands
from discord.ui import Select, View
import random


class battleSystem(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.enemy = None
        self.enemy_HP = 1
                
    @commands.Cog.listener()
    async def on_ready(self):
        print("Loading cog: battle.py")

    @commands.command()
    async def battle(self, ctx):
        if self.client.job == None:
            await ctx.send("You have not selected a job. Use `.start` command")

        elif self.enemy:
            embed_message=discord.Embed(title=f"The {self.enemy['name']} didn't hear no bell.")
            embed_message.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            embed_message.set_image(url=self.enemy['image'])
            embed_message.set_footer(text=f"What will you do? Distance is {self.client.combat_skills.distance}. Your HP is {self.client.hp}. Enemy HP is {self.enemy_HP}.")

            select_menu = Select(options=[])
            for item in self.client.job["skills"].values():
                select_menu.append_option(discord.SelectOption(
                    label=item
                ))
            
            async def callback(interaction):
                # select_menu.values is simply an array of selections made by the user
                # user can only choose 1 option so we use the first and only value in the array
                message, damage = getattr(self.client.combat_skills, select_menu.values[0])()  # calls a function in skills.py class with the same name
                self.enemy_HP -= damage
                if self.enemy_HP <= 0:
                    await interaction.response.send_message(f"The {self.enemy['name']} is slain!")
                    self.enemy = None
                else:
                    embed_message=discord.Embed(title=message)
                    embed_message.add_field(value=message, inline=True)
                    embed_message.add_field(value=message, inline=True)
                    embed_message.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
                    embed_message.set_image(url=self.enemy['image'])
                    embed_message.set_footer(text=f"What will you do? Distance is {self.client.combat_skills.distance}. Your HP is {self.client.hp}. Enemy HP is {self.enemy_HP}.")

                    select_menu.callback = callback
                    view = View()
                    view.add_item(select_menu)
                    await interaction.response.send_message(embed=embed_message, view=view, ephemeral=False)

            select_menu.callback = callback
            view = View()
            view.add_item(select_menu)
            await ctx.send(embed=embed_message, view=view, ephemeral=False)

        else:    
            self.enemy = random.choice(self.client._spawns['mobs'])
            self.enemy_HP = self.enemy['HP']
            embed_message=discord.Embed(
                title=f"The {self.enemy['name']} ambushes you!")
            
            embed_message.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            embed_message.set_image(url=self.enemy['image'])
            embed_message.set_footer(text=f"What will you do? Distance is {self.client.combat_skills.distance}. Your HP is {self.client.hp}. Enemy HP is {self.enemy_HP}.")

            select_menu = Select(options=[])
            for item in self.client.job["skills"].values():
                select_menu.append_option(discord.SelectOption(
                    label=item
                ))
            
            async def callback(interaction):
                # select_menu.values is simply an array of selections made by the user
                # user can only choose 1 option so we use the first and only value in the array
                p_message, e_damage = getattr(self.client.combat_skills, select_menu.values[0])()  # calls a function in skills.py class with the same name
                e_message, p_damage = getattr(self.client.combat_skills, random.choice(self.enemy['skills']))()
                self.enemy_HP -= e_damage
                self.client.hp -= p_damage
                if self.enemy_HP <= 0:
                    await interaction.response.send_message(f"The {self.enemy['name']} is slain!")
                    self.enemy = None
                elif self.client.hp <= 0:
                    await interaction.response.send_message(f"You died!")
                    self.client.job = None
                    self.client.level = 1
                    self.client.hp = 100
                    self.enemy = None
                else:
                    embed_message=discord.Embed(title=p_message, color=discord.Color.red())
                    embed_message.add_field(name="Player", value=p_message, inline=True)
                    embed_message.add_field(name="Enemy", value=e_message, inline=True)
                    embed_message.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
                    embed_message.set_image(url=self.enemy['image'])
                    embed_message.set_footer(text=f"What will you do? Distance is {self.client.combat_skills.distance}. Your HP is {self.client.hp}. Enemy HP is {self.enemy_HP}.")

                    select_menu.callback = callback
                    view = View()
                    view.add_item(select_menu)
                    await interaction.response.send_message(embed=embed_message, view=view, ephemeral=False)

            select_menu.callback = callback
            view = View()
            view.add_item(select_menu)
            await ctx.send(embed=embed_message, view=view, ephemeral=False)

async def setup(client):
	await client.add_cog(battleSystem(client))
