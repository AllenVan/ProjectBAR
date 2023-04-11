import discord
from discord.ext import commands


class Spawn(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.user_class = None
                
    @commands.Cog.listener()
    async def on_ready(self):
        print("Loading cog: battle.py")

    @commands.command()
    async def spawn(self, ctx):
        embed_message=discord.Embed(
            title="An Apple of Rizz Ambushes you!")

        embed_message.set_image(url="https://i.imgflip.com/74n62t.jpg")
        # embed.add_field(name="Field 1 Title", value="This is the value for field 1. This is NOT an inline field.", inline=False)
        # embed.add_field(name="Field 2 Title", value="It is inline with Field 3", inline=True)
        # embed.add_field(name="Field 3 Title", value="It is inline with Field 2", inline=True)
        embed_message.set_footer(text="What will you do?")
        await ctx.send(embed=embed_message, view=SelectAction(self), ephemeral=True)

class SelectAction(discord.ui.View):
	def __init__(self, user: Spawn):
		super().__init__()
		self.user = user

	@discord.ui.button(label="Fight", style=discord.ButtonStyle.blurple)
	async def fight_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.send_message(f"HIT", ephemeral=True)

	@discord.ui.button(label="Block", style=discord.ButtonStyle.blurple)
	async def block_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.send_message(f"DEFENSIVE POSITIONS", ephemeral=True)

	@discord.ui.button(label="Run", style=discord.ButtonStyle.blurple)
	async def run_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.send_message(f"CAN'T ESCAPE", ephemeral=True)

async def setup(client):
	await client.add_cog(Spawn(client))
