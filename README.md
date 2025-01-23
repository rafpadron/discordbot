# Guebot - Cyberpunk Discord Bot

A versatile Discord bot with AI capabilities, including chat, image generation, weather information, and moderation features. The bot takes on the persona of a cyberpunk antihero named Guebot, whose mission is to end corruption in the city.

## Features

- **AI Chat**: Engage in conversations with Guebot using Google's Gemini AI
- **Image Generation**: Create AI-generated images using Stability AI
- **Weather Information**: Get current weather data for any city
- **Message Management**: Clear chat messages with ease
- **Auto-Translation**: Automatically translates Spanish prompts to English for image generation

## Setup

1. Clone this repository
2. Install the required dependencies:
```bash
pip install discord.py python-dotenv requests google-generativeai openai
```

3. Create a `.env` file in the root directory with the following variables:
```env
DISCORD_TOKEN=your_discord_bot_token
GEMINI_API_KEY=your_gemini_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
STABILITY_API_KEY=your_stability_api_key
```

4. Run the bot:
```bash
python main.py
```

## Commands

### Basic Commands
- `.hello` - Get a greeting from Guebot
- `.chat <message>` - Chat with Guebot using AI

### Image Generation
- `.imagine <prompt>` - Generate an image from your description
  - Works in both English and Spanish
  - Automatically translates Spanish prompts to English
  - Creates high-quality 1024x1024 images

### Weather Information
- `.weather <city>` - Get current weather information for any city
  - Shows temperature, feels like, humidity, and wind speed
  - Uses metric units (Celsius, m/s)

### Moderation
- `.clear <number>` - Delete a specified number of messages
  - Requires "Manage Messages" permission
  - Maximum 100 messages per command
  - Confirmation message auto-deletes after 5 seconds

### Mentions
- The bot will respond when mentioned in a message

## Required Permissions

The bot requires the following Discord permissions:
- Read Messages
- Send Messages
- Manage Messages (for the clear command)
- View Channels
- Embed Links (for sending images)

## Error Handling

The bot includes comprehensive error handling for:
- API failures
- Permission issues
- Invalid inputs
- Network problems

## Notes

- All image generation prompts are automatically translated to English for better results
- The bot has a character limit of 100 messages for the clear command to prevent accidental mass deletions
- Weather data is provided in metric units
- The bot maintains its cyberpunk antihero persona across all interactions

## Support

If you encounter any issues or need help, please open an issue in this repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
