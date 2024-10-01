from config import status, owners, TOKEN
from api import SuperViveAPI
from datetime import *
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
        super().__init__(owner_ids=set(owners), intents=intents) 
        self.persistent_views_added = False

    async def on_ready(self):
        if not self.persistent_views_added:
            self.persistent_views_added = True
        print(f'Logged in as {self.user}')
        change_status.start()
        
act_status = 0
@tasks.loop(seconds=60)
async def change_status():
    global act_status
    if act_status == len(status):
        act_status = 0
    await bot.change_presence(activity=discord.Game(name=status[act_status]))
    act_status += 1
    

bot = Vue_persistante()
api = SuperViveAPI()
bot.remove_command("help")


@bot.slash_command(name="tierlist", description="Get the tierlist for a specific gamemode")
@option("gamemode", str, description="The gamemode to get the tierlist for", required=True, choices=["Squad", "Duos", "DeathMatch"])
@option("sort", str, description="Sort the tierlist by a specific stat", choices=["Winrate", "Pickrate", "KD"], required=False)
async def tierlist(ctx, gamemode: str, sort: str = "Winrate"):
    try:
        await ctx.defer()
        sort_key = ""
        if sort == "Winrate":
            sort_key = "wr1"
        elif sort == "Pickrate":
            sort_key = "pr"
        elif sort == "kd":
            sort_key = "kd"
        
        if gamemode == "DeathMatch":
            gamemode = "dm"
        elif gamemode == "BRDuos":
            gamemode = "duo"
        elif gamemode == "BRSquad":
            gamemode = "squad"
        
        tierlist = api.statistics(gamemode)
        if not tierlist:
            await ctx.respond("No tierlist found for that gamemode.")
            return
        
        if sort_key in ["wr1", "pr"]:
            tierlist.sort(key=lambda x: x[sort_key]['v'], reverse=True)
        else:
            tierlist.sort(key=lambda x: x[sort_key], reverse=True)

        embeds = []
        embed = discord.Embed(title=f"Tierlist for {gamemode} (Sorted by {sort})", color=0x00ff00)

        for i, hero in enumerate(tierlist):
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

            if (i + 1) % 8 == 0:
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
        
        if selected_hero == "Overall Stats":
            embed = create_player_stats_embed(self.player_stats, self.player_id, self.player_name)
        else:
            filtered_stats = [game for game in self.player_stats if game['hero'] == selected_hero]

            embed = discord.Embed(title="Player Stats", description=f"Stats for player:  **__{self.player_name}__** \nHero: **__{selected_hero}__**", color=0x00ff00)
            embed.set_footer(text=f"Player ID: {self.player_id}")
            hero_image_url = api.get_hero_images(selected_hero)
            embed.set_thumbnail(url=hero_image_url)
            
            total_kills = sum(game['kills'] for game in filtered_stats)
            total_time_played = sum(game['timePlayedSeconds'] for game in filtered_stats)
            total_damage_dealt = sum(game['heroDamageDealt'] for game in filtered_stats)
            total_healing_given = sum(game['healingGiven'] for game in filtered_stats)
            
            hours, remainder = divmod(total_time_played, 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_time = f"{hours}h {minutes}m {seconds}s"
            
            embed.add_field(name="Total Kills", value=total_kills, inline=True)
            embed.add_field(name="Total Time Played", value=formatted_time, inline=True)
            embed.add_field(name="Total Damage Dealt", value=total_damage_dealt, inline=True)
            embed.add_field(name="Total Healing Given", value=total_healing_given, inline=True)
            
            for game in filtered_stats:
                embed.add_field(name=f"Queue: {game['queue']}", value=f"Games Played: {game['gamesPlayed']}\nWins: {game['won']}\nKills: {game['kills']}\nDeaths: {game['deaths']}", inline=False)

        await interaction.response.edit_message(embed=embed, view=self.view)


def create_player_stats_embed(player_stats, player_id, player_name):
    aggregate_stats = {
        "timePlayedSeconds": 0,
        "kills": 0,
        "knocks": 0,
        "deaths": 0,
        "revives": 0,
        "resurrects": 0,
        "creepKills": 0,
        "goldEarned": 0,
        "heroDamageDealt": 0,
        "heroDamageTaken": 0,
        "healingGiven": 0,
    }

    for game in player_stats:
        aggregate_stats["timePlayedSeconds"] += game["timePlayedSeconds"]
        aggregate_stats["kills"] += game["kills"]
        aggregate_stats["knocks"] += game["knocks"]
        aggregate_stats["deaths"] += game["deaths"]
        aggregate_stats["revives"] += game["revives"]
        aggregate_stats["resurrects"] += game["resurrects"]
        aggregate_stats["creepKills"] += game["creepKills"]
        aggregate_stats["goldEarned"] += game["goldEarned"]
        aggregate_stats["heroDamageDealt"] += game["heroDamageDealt"]
        aggregate_stats["heroDamageTaken"] += game["heroDamageTaken"]
        aggregate_stats["healingGiven"] += game["healingGiven"]

    total_time_seconds = aggregate_stats["timePlayedSeconds"]
    hours, remainder = divmod(total_time_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time = f"{hours}h {minutes}m {seconds}s"

    embed = discord.Embed(title="Player Stats", description=f"Stats for player: **__{player_name}__**", color=0x00ff00)
    embed.add_field(name="Total Time Played", value=formatted_time, inline=False)
    embed.add_field(name="Total Kills", value=aggregate_stats["kills"], inline=True)
    embed.add_field(name="Total Knocks", value=aggregate_stats["knocks"], inline=True)
    embed.add_field(name="Total Deaths", value=aggregate_stats["deaths"], inline=True)
    embed.add_field(name="Total Revives", value=aggregate_stats["revives"], inline=True)
    embed.add_field(name="Total Resurrects", value=aggregate_stats["resurrects"], inline=True)
    embed.add_field(name="Total Creep Kills", value=aggregate_stats["creepKills"], inline=True)
    embed.add_field(name="Total Gold Earned", value=aggregate_stats["goldEarned"], inline=True)
    embed.add_field(name="Total Hero Damage Dealt", value=aggregate_stats["heroDamageDealt"], inline=True)
    embed.add_field(name="Total Hero Damage Taken", value=aggregate_stats["heroDamageTaken"], inline=True)
    embed.add_field(name="Total Healing Given", value=aggregate_stats["healingGiven"], inline=True)
    embed.set_footer(text=f"Player ID: {player_id}")

    return embed

async def player_autocomplete(ctx: discord.AutocompleteContext):
    try:
        player_name = ctx.value
        search_results = api.search(player_name) if player_name else []
        return [
            discord.OptionChoice(
                name=result.get('d', f"Player {result.get('u', 'Unknown')}"),
                value=result.get('d', 'Unknown')
            ) for result in search_results if 'u' in result and 'd' in result
        ]
    except Exception as e:
        logging.error(f"Error in autocomplete: {e}")
        return []

@bot.slash_command(name="stats", description="Get stats of a player")
@option("player", str, description="Name of the player to get the stats of", required=True, autocomplete=player_autocomplete)
async def stats(ctx, player: str):
    try:
        await ctx.defer()
        
        search_results = api.search(player)
        if not search_results:
            await ctx.respond("Player not found.")
            return
        
        player_data = search_results[0]  # Assuming the first result is the desired player
        player_id = player_data['u']
        player_name = player_data['d']
        
        player_stats = api.get_player_stats(player_id)
        
        if not player_stats:
            await ctx.respond("No stats found for that player.")
            return

        heroes = {game['hero'] for game in player_stats}
        hero_options = [discord.SelectOption(label="Overall Stats", value="Overall Stats")] + [discord.SelectOption(label=hero, value=hero) for hero in heroes]

        hero_select = HeroSelect(hero_options, player_stats, player_id, player_name)
        view = View()
        view.add_item(hero_select)
        
        embed = create_player_stats_embed(player_stats, player_id, player_name)

        await ctx.respond(embed=embed, content=f"Select a hero from the list for {player_name}:", view=view)
    except Exception as e:
        logging.error(f"Error in stats command: {e}")
        await ctx.respond("An error occurred while fetching stats. Please try again later.")



if __name__ == "__main__":
    bot.run(TOKEN)
