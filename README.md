# discord-fact-check
A discord bot to fact check directly from discord UI

## Description
A Discord Bot which installs to user profile and adds feature to fact check messages by utilising Tavily and Openrouter. It integrates natively into Discord UI, allowing easy usage in servers.

## Features

- **User Installed** Integrates into the Discord native UI. Right clicking any text message, then Apps, then Fact-Check allows easy usage.
- **Uses Tavily** Search queries are routed through Tavily API.
- **Uses OpenRouter** AI summary queries are routed through OpenRouter API.
- **Asynchronous Handling** Handles incoming traffic using thread locks for better stability.
- **Ephemeral Response:** Responses are delivered using ephemeral interactions, resulting in the verification result remaining visible only to the person who triggered the command.

## Setup

1. Get API keys for Discord bot at [Discord Developer Portal](https://discord.com/developers/), AI gateway and Tavily.

2. Clone the repo

3. **Create and activate a virtual environment:**
   * **macOS/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   * **Windows:**
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
4. **Change `.env.example` to `.env` with the following keys-**
    * Discord token specific for a bot
    * AI gateway API key
    * AI gateway server URL
    * Tavily API Key

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Once setup is verified, `main.py` can be run to start the discord bot.
