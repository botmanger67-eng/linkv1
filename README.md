# DuckDuckGo Telegram Bot

A powerful Telegram bot that searches DuckDuckGo for web results, images, news, and instant answers - all without requiring any API keys!

## Features

- 🔍 **Web Search** - Get relevant web search results
- 🖼️ **Image Search** - Find and retrieve images
- 📰 **News Search** - Stay updated with latest news
- ⚡ **Instant Answers** - Get quick answers to your queries
- 🎯 **Safe Search** - Optional safe search filtering
- 🌐 **Multi-language Support** - Search in different languages
- 📱 **User-friendly** - Simple and intuitive commands

## Prerequisites

- Python 3.7 or higher
- A Telegram account
- A Telegram Bot Token (get it from [@BotFather](https://t.me/botfather))

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/duckduckgo-telegram-bot.git
cd duckduckgo-telegram-bot
```

### 2. Create a Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
BOT_TOKEN=your_telegram_bot_token_here
```

Or set the environment variable directly:

```bash
# On Windows (Command Prompt)
set BOT_TOKEN=your_telegram_bot_token_here

# On Windows (PowerShell)
$env:BOT_TOKEN="your_telegram_bot_token_here"

# On macOS/Linux
export BOT_TOKEN="your_telegram_bot_token_here"
```

## Usage

### Running the Bot

```bash
python bot.py
```

The bot will start polling and be ready to accept commands.

### Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and see welcome message |
| `/help` | Show help information |
| `/web <query>` | Search the web |
| `/images <query>` | Search for images |
| `/news <query>` | Search for news |
| `/answer <query>` | Get instant answers |
| `/settings` | Configure bot settings |

### Examples

```
/web Python programming tutorials
/images beautiful sunset landscape
/news latest technology trends
/answer What is the capital of France?
```

## Project Structure

```
duckduckgo-telegram-bot/
├── bot.py              # Main bot application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in repo)
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## Dependencies

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [duckduckgo_search](https://github.com/deedy5/duckduckgo_search) - DuckDuckGo search library
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Environment variable management

## Configuration

### Bot Settings

Users can configure the following settings via `/settings`:

- **Safe Search**: Enable/disable safe search filtering
- **Language**: Set preferred search language
- **Results Limit**: Set number of results to display (1-10)

### Advanced Configuration

You can modify the following in `bot.py`:

```python
# Default settings
DEFAULT_SAFE_SEARCH = True
DEFAULT_LANGUAGE = "en"
DEFAULT_RESULTS_LIMIT = 5
```

## Error Handling

The bot includes comprehensive error handling:

- Network errors during search
- Invalid queries
- Rate limiting
- Bot token validation
- User input validation

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Check code style
flake8
```

## Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check if BOT_TOKEN is set correctly
   - Ensure internet connection
   - Verify bot is running

2. **Search results not showing**
   - Check DuckDuckGo availability
   - Try different search terms
   - Disable safe search if needed

3. **Rate limiting**
   - Wait a few seconds between requests
   - Reduce results limit

### Logs

The bot logs information to console. Run with debug mode for more details:

```bash
python bot.py --debug
```

## Security

- No API keys required
- All searches are anonymous
- No user data is stored
- HTTPS for all communications

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [DuckDuckGo](https://duckduckgo.com/) for their privacy-focused search engine
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) team
- [duckduckgo_search](https://github.com/deedy5/duckduckgo_search) library developers

## Support

For support, please:

- Open an [issue](https://github.com/yourusername/duckduckgo-telegram-bot/issues)
- Check the [FAQ](https://github.com/yourusername/duckduckgo-telegram-bot/wiki/FAQ)
- Join our [Telegram group](https://t.me/your_bot_support_group)

## Roadmap

- [ ] Add voice search support
- [ ] Implement inline mode
- [ ] Add custom search filters
- [ ] Support for multiple languages
- [ ] Add caching for faster results
- [ ] Web interface for configuration

---

**Made with ❤️ by [Your Name]**

*Note: This bot is not affiliated with DuckDuckGo or Telegram.*