import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests
import google.generativeai as genai
from google.generativeai import types
from openai import OpenAI
import base64
import asyncio

# Load environment variables from .env file
load_dotenv()

# Get the tokens from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
STABILITY_API_KEY = os.getenv('STABILITY_API_KEY')
# Configure your Gemini API key
genai.configure(api_key=GEMINI_API_KEY)
# Configure the Discord bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guild_messages = True  # Required for message deletion

bot = commands.Bot(command_prefix=".", intents=intents)

# Bot startup event
@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

# Basic command
@bot.command()
async def hello(ctx):
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction="you are an antihero from a cyberpunk world, your name is Guebot and your mission is to end corruption in the city")
    response = model.generate_content("hello")
    await ctx.send(response.text)

# Text generation command
@bot.command()
async def chat(ctx, *, prompt: str):
    """Generates a response using Gemini"""
    try:
        print(f"Generating response for: {prompt}")
        # Generate text with Gemini
        model = genai.GenerativeModel("gemini-1.5-flash", system_instruction="you are an antihero from a cyberpunk world, your name is Guebot and your mission is to end corruption in the city")
        response = model.generate_content(prompt)
        # Send the generated response
        await ctx.send(response.text)
    except Exception as e:
        print(f"Error: {e}")
        await ctx.send("There was an error generating the response.")

# Image generation command
@bot.command()
async def imagine(ctx, *, prompt: str):
    """Generates an image using Stability AI"""
    try:
        await ctx.send(f"Generating image for: `{prompt}`. Please wait!")
        
        # Translate prompt to English using Gemini
        model = genai.GenerativeModel("gemini-1.5-flash")
        translation_prompt = f"Translate the following Spanish text to English, only return the translation without any additional text or context: {prompt}"
        translation = model.generate_content(translation_prompt)
        english_prompt = translation.text.strip()
        
        await ctx.send(f"Translated prompt: `{english_prompt}`")
        
        response = requests.post(
            "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {STABILITY_API_KEY}"
            },
            json={
                "text_prompts": [
                    {
                        "text": english_prompt,
                        "weight": 1
                    }
                ],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
            },
        )

        if response.status_code != 200:
            await ctx.send(f"Error generating the image: {response.text}")
            return

        data = response.json()
        
        # Get the base64 image from the response
        image_data = base64.b64decode(data["artifacts"][0]["base64"])
        
        # Save the image temporarily
        with open("generated_image.png", "wb") as f:
            f.write(image_data)
        
        # Send the image
        await ctx.send(file=discord.File("generated_image.png"))
        
        # Clean up the temporary file
        os.remove("generated_image.png")
        
    except Exception as e:
        print(f"Error: {e}")
        await ctx.send("There was an error generating the image. Please try again.")

# Weather command
@bot.command()
async def weather(ctx, *, city: str):
    """Gets the current weather for a city"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=en"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            await ctx.send(f"Error getting weather: {data['message']}")
            return

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        weather_report = (
            f"Weather in {city}:\n"
            f"Description: {weather}\n"
            f"Temperature: {temp}°C\n"
            f"Feels like: {feels_like}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )
        await ctx.send(weather_report)
    except Exception as e:
        print(f"Error: {e}")
        await ctx.send("There was an error getting the weather.")

# Clear command
@bot.command()
async def clear(ctx, amount: int = None):
    """Clears messages from the chat. Usage: .clear <number of messages>"""
    try:
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send("You don't have permission to delete messages.")
            return
            
        if amount is None:
            await ctx.send("Please specify how many messages you want to delete. Example: `.clear 10`")
            return
            
        if amount <= 0:
            await ctx.send("Please specify a positive number of messages.")
            return
            
        # Limit maximum number of messages to delete to prevent accidents
        if amount > 100:
            await ctx.send("For safety, you can only delete up to 100 messages at once.")
            amount = 100
            
        # Delete the command message
        await ctx.message.delete()
        
        # Delete the specified messages
        deleted = await ctx.channel.purge(limit=amount)
        
        # Send confirmation
        confirm_msg = await ctx.send(f"✅ {len(deleted)} messages have been deleted.")
        
        # Delete confirmation message after 5 seconds
        await asyncio.sleep(5)
        await confirm_msg.delete()
        
    except discord.Forbidden:
        await ctx.send("I don't have permission to delete messages. Make sure I have the 'Manage Messages' permission.")
    except Exception as e:
        print(f"Error deleting messages: {e}")
        await ctx.send("An error occurred while trying to delete messages.")

# Respond to mentions
@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        model = genai.GenerativeModel("gemini-1.5-flash", system_instruction="you are an antihero from a cyberpunk world, your name is Guebot and your mission is to end corruption in the city")
        response = model.generate_content("hey you")
        await message.channel.send(response.text)
    await bot.process_commands(message)

# Run the bot
bot.run(DISCORD_TOKEN)
