from apikeys import *
import discord
from discord import app_commands
from discord.ext import commands
import requests
import mysql.connector

intents = discord.Intents.default()
client = commands.Bot(command_prefix=prefix, intents=intents)

@client.event
async def on_ready():
    print(client.user)
    print(client.user.id)
    print('------------------------------')
    try:
        synced = await client.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)


class Choice(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose your cow !", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Vache1",
                description="description de la vache 1"
            ),
            discord.SelectOption(
                label="Vache2",
                description="description de la vache 2"
            )
        ]
    )

    async def select_callback(self, interaction, select): 
        db = mysql.connector.connect(
            host=host_,
            user=user_,
            passwd=passwd_,
            database=database_ 
        )

        mycursor = db.cursor()
    
        select.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"Vous avez choisi {select.values[0]}!", ephemeral=True)
        mycursor.execute("INSERT INTO players (id) VALUES (%s)", (str(interaction.user.id), ))
        db.commit()

        # mycursor.execute("INSERT INTO players (cows_owned) SELECT %s FROM interaction WHERE username = %s", (select.values[0], interaction.user.name))
"""
@client.tree.command(name='help',description='Get help :3')
async def help(interaction: discord.Interaction):
    help_message = (
        "/all = \n" +
        "\n"
    )
    await interaction.response.send_message()
"""

@client.tree.command(name='start',description='Choose your first cow ^^')
async def start(interaction: discord.Interaction):
    embed = discord.Embed(title ='Choose your cow ^^',
        color = 0xB48EAD)
    embed.set_image(url = 'https://mktg.factosoft.com/consoglobe/image-upload/img/vache-laitiere.jpg')
    embed2 = discord.Embed()
    embed2.set_image(url='https://www.mangeons-local.bzh/wp-content/uploads/alimentation-vache.jpg')
    await interaction.response.send_message( embeds=[embed, embed2], view=Choice())
    


   
@client.tree.command(name='all', description='All cows available ^^')
async def all(interaction: discord.Interaction):
    db = mysql.connector.connect(
        host=host_,
        user=user_,
        passwd=passwd_,
        database=database_ 
    )

    mycursor = db.cursor()

    mycursor.execute("SELECT race FROM cows")
    
    races = ""
    for x in mycursor :
        races += x[0] + '\n'

    await interaction.response.send_message(races)


client.run(token)
