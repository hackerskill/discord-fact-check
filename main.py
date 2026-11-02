import json
import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from tavily import TavilyClient

load_dotenv()
 
token = os.getenv("DISCORD_TOKEN")
tavily_client = TavilyClient(api_key=os.getenv("WEB_SEARCH_API_KEY"))
response = tavily_client.search("Who is Leo Messi?")

print(response)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree= app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}", flush=True)

@tree.context_menu(name="Fact Check")
async def clear(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.defer(ephemeral=True)
    claim=message.content.strip()
    response = tavily_client.search(claim)

    text = json.dumps(response)
    output = f"```json\n{text[:1950]}\n```"

    await interaction.followup.send(f"Fact Check Result: {output}", ephemeral=True)

@tree.command(name="about", description="Get information about this chatbot")
async def about(interaction: discord.Interaction):
    await interaction.response.send_message("This is a Discord Bot which can be used to instantly fact check any information.")

client.run(token)
