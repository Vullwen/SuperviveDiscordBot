from config import status, owners, TOKEN
from api import SuperViveAPI
from datetime import *
import re
import logging

import discord
from discord import option, slash_command
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, tasks
from discord.utils import get
from discord.ui import Button, View, Select

intents = discord.Intents.all()
intents.emojis = True
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True
logging.basicConfig(level=logging.INFO)

class Vue_persistante(commands.Bot):
    def __init__(self):
        super().__init__(owner_ids=set(owners), intents=intents)  # Préfixe du bot
        self.persistent_views_added = False

    async def on_ready(self):
        if not self.persistent_views_added:
            self.persistent_views_added = True
        print(f'Logged in as {self.user}')

bot = Vue_persistante()
api = SuperViveAPI()
bot.remove_command("help")


@bot.slash_command(name="tierlist", description="Get the tierlist for a specific gamemode")
@option("gamemode", str, description="The gamemode to get the tierlist for", required=True, choices=["BRSquad", "BRDuos", "DM"])
@option("sort", str, description="Sort the tierlist by a specific stat", choices=["Winrate", "Pickrate", "kd"], required=False)
async def tierlist(ctx, gamemode: str, sort: str = "Winrate"):
    try:
        await ctx.defer()
        if sort == "Winrate":
            sorted_heroes = "wr1"
        elif sort == "Pickrate":
            sorted_heroes = "pr"
        elif sort == "kd":
            sorted_heroes = "kd"
        
        tierlist = api.statistics(gamemode, sort=sorted_heroes)
        if not tierlist:
            await ctx.respond("No tierlist found for that gamemode.")
            return

        embeds = []
        embed = discord.Embed(title=f"Tierlist for {gamemode} (Sorted by {sort})", color=0x00ff00)

        for i, hero in enumerate(tierlist):
            hero_image = api.get_hero_images(hero['h'])
            embed.add_field(
                name=hero['h'],
                value=f"Win Rate: {hero['wr1']['v']*100:.2f}%",
                inline=True
            )
            embed.add_field(
                name="\u200b",
                value=f"Pick Rate: {hero['pr']['v']*100:.2f}%",
                inline=True
            )
            embed.add_field(
                name="\u200b",
                value=f"K/D: {hero['kd']:.2f}",
                inline=True
            )

            if (i + 1) % 8 == 0 or i == len(sorted_heroes) - 1:
                embeds.append(embed)
                embed = discord.Embed(color=0x00ff00)

        for e in embeds:
            await ctx.respond(embed=e)
    except Exception as e:
        logging.error(f"Error in tierlist command: {e}")
        await ctx.respond("An error occurred while fetching tierlist. Please try again later.")



class HeroSelect(Select):
    def __init__(self, options, player_stats, player_id, player_name):
        self.player_stats = player_stats
        self.player_id = player_id
        self.player_name = player_name
        super().__init__(placeholder="Choose a hero...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_hero = self.values[0]
        filtered_stats = [game for game in self.player_stats if game['hero'] == selected_hero]

        embed = discord.Embed(title="Player Stats", description=f"Stats for player:  **__{self.player_name}__** \nHero: **__{selected_hero}__**", color=0x00ff00)
        embed.set_footer(text=f"Player ID: {self.player_id}")
        hero_image_url = api.get_hero_images(selected_hero)
        embed.set_thumbnail(url=hero_image_url)
        
        for game in filtered_stats:
            embed.add_field(name=f"Queue: {game['queue']}", value=f"Games Played: {game['gamesPlayed']}\nWins: {game['won']}\nKills: {game['kills']}\nDeaths: {game['deaths']}", inline=False)

        await interaction.response.edit_message(embed=embed, view=self.view)

async def player_autocomplete(ctx: discord.AutocompleteContext):
    try:
        player_name = ctx.value
        search_results = api.search(player_name) if player_name else []
        return [
            discord.OptionChoice(
                name=result.get('d', f"Player {result.get('u', 'Unknown')}"),
                value=f"{result['u']}|{result['d']}"
            ) for result in search_results if 'u' in result and 'd' in result
        ]
    except Exception as e:
        logging.error(f"Error in autocomplete: {e}")
        return []

@bot.slash_command(name="stats", description="Get stats of a player")
@option("player", str, description="Name or ID of the player to get the stats of", required=True, autocomplete=player_autocomplete)
async def stats(ctx, player: str):
    try:
        await ctx.defer()
        
        player_id, player_name = player.split('|')
        
        player_stats = api.get_player_stats(player_id)
        
        if not player_stats:
            await ctx.respond("No stats found for that player.")
            return

        heroes = {game['hero'] for game in player_stats}
        hero_options = [discord.SelectOption(label=hero, value=hero) for hero in heroes]

        hero_select = HeroSelect(hero_options, player_stats, player_id, player_name)
        view = View()
        view.add_item(hero_select)

        await ctx.respond(f"Select a hero from the list for {player_name}:", view=view)
    except Exception as e:
        logging.error(f"Error in stats command: {e}")
        await ctx.respond("An error occurred while fetching stats. Please try again later.")

if __name__ == "__main__":
    bot.run(TOKEN)
