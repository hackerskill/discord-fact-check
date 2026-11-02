import json
import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from openrouter import OpenRouter
from tavily import TavilyClient
import asyncio

load_dotenv()
 
token = os.getenv("DISCORD_TOKEN")
tavily_client = TavilyClient(api_key=os.getenv("WEB_SEARCH_API_KEY"))

current_model="nvidia/nemotron-3.5-lightning:free"

lock= asyncio.Lock()
tokens_limit=10000

ai_client = OpenRouter(
    api_key=os.getenv("AI_API_KEY"),
    server_url=os.getenv("AI_SERVER_URL"),
)

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
    search_response = tavily_client.search(claim)


    async with lock:
        try:
            async with asyncio.timeout(60):

                    web_context=json.dumps(search_response, indent=2)
                    system_instruction = "You are a factual verification bot. Check if the user's claim matches the web search metrics."
                    user_payload = f"Claim to verify: {claim}\n\nSearch Data Context:\n{web_context}"
                    print("payload prepared, sending to openrouter", flush=True)
                    
                    response = await asyncio.to_thread(
                        ai_client.chat.send,
                        model=current_model,
                        messages=[
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": user_payload}
                        ],
                        max_tokens=tokens_limit,
                        stream=False,
                )
                    print("response received from openrouter", flush=True)
        except TimeoutError:
            print("AI request timed out", flush=True)
            await interaction.followup.send("Request timed out. Please try again later.")
            return

        except Exception as e:
            print(f"Error occurred: {e}", flush=True)
            await interaction.followup.send("An error occurred while processing your request. Please try again later.")
            return

        if not response.choices or not response.choices[0].message:
            print("No valid response received from OpenRouter", flush=True)
            await interaction.followup.send("No valid response received from the AI model. Please try again later.")
            return

        await interaction.followup.send(f"Fact Check Result: {response.choices[0].message.content}", ephemeral=True)

@tree.command(name="about", description="Get information about this chatbot")
async def about(interaction: discord.Interaction):
    await interaction.response.send_message("This is a Discord Bot which can be used to instantly fact check any information.")

client.run(token)
