import logging
import os
from typing import Optional, List, Dict, Any

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
from duckduckgo_search import DDGS

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
MAX_RESULTS = 5  # Maximum number of results per search

# Search types
SEARCH_TYPES = {
    "web": "🌐 Web",
    "images": "🖼️ Images",
    "news": "📰 News",
    "answers": "💡 Instant Answers",
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the /start command is issued."""
    user = update.effective_user
    welcome_text = (
        f"👋 Hello {user.first_name}!\n\n"
        "I'm a DuckDuckGo search bot. I can search the web, images, news, "
        "and provide instant answers without any API key.\n\n"
        "🔍 Just send me a query to start searching!\n"
        "💡 Use /help to see all available commands."
    )
    await update.message.reply_text(welcome_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message when the /help command is issued."""
    help_text = (
        "🤖 *DuckDuckGo Search Bot Help*\n\n"
        "*Commands:*\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/search `<query>` - Search the web\n"
        "/images `<query>` - Search for images\n"
        "/news `<query>` - Search for news\n"
        "/answer `<query>` - Get instant answers\n\n"
        "*Usage:*\n"
        "Simply send any text message to search the web by default.\n"
        "Use the buttons below search results to switch between search types.\n\n"
        "*Note:* Results are limited to 5 per search for readability."
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def search_web(query: str, max_results: int = MAX_RESULTS) -> List[Dict[str, Any]]:
    """Search the web using DuckDuckGo."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return results
    except Exception as e:
        logger.error(f"Error searching web: {e}")
        return []


async def search_images(query: str, max_results: int = MAX_RESULTS) -> List[Dict[str, Any]]:
    """Search for images using DuckDuckGo."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(query, max_results=max_results))
            return results
    except Exception as e:
        logger.error(f"Error searching images: {e}")
        return []


async def search_news(query: str, max_results: int = MAX_RESULTS) -> List[Dict[str, Any]]:
    """Search for news using DuckDuckGo."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(query, max_results=max_results))
            return results
    except Exception as e:
        logger.error(f"Error searching news: {e}")
        return []


async def search_answers(query: str) -> Optional[Dict[str, Any]]:
    """Get instant answers from DuckDuckGo."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.answers(query))
            return results[0] if results else None
    except Exception as e:
        logger.error(f"Error getting instant answers: {e}")
        return None


def format_web_results(results: List[Dict[str, Any]]) -> str:
    """Format web search results into a readable message."""
    if not results:
        return "❌ No results found."

    message = "🌐 *Web Search Results:*\n\n"
    for i, result in enumerate(results, 1):
        title = result.get("title", "No title")
        body = result.get("body", "No description")
        href = result.get("href", "")
        message += f"*{i}. {title}*\n{body}\n[Link]({href})\n\n"
    return message


def format_image_results(results: List[Dict[str, Any]]) -> str:
    """Format image search results into a readable message."""
    if not results:
        return "❌ No images found."

    message = "🖼️ *Image Search Results:*\n\n"
    for i, result in enumerate(results, 1):
        title = result.get("title", "No title")
        image_url = result.get("image", "")
        source = result.get("url", "")
        message += f"*{i}. {title}*\n[View Image]({image_url}) | [Source]({source})\n\n"
    return message


def format_news_results(results: List[Dict[str, Any]]) -> str:
    """Format news search results into a readable message."""
    if not results:
        return "❌ No news found."

    message = "📰 *News Search Results:*\n\n"
    for i, result in enumerate(results, 1):
        title = result.get("title", "No title")
        body = result.get("body", "No description")
        url = result.get("url", "")
        source = result.get("source", "Unknown source")
        date = result.get("date", "Unknown date")
        message += f"*{i}. {title}*\n{body}\nSource: {source} | Date: {date}\n[Link]({url})\n\n"
    return message


def format_answer_result(result: Optional[Dict[str, Any]]) -> str:
    """Format instant answer result into a readable message."""
    if not result:
        return "❌ No instant answer found."

    answer = result.get("text", "No answer available")
    topic = result.get("topic", "")
    message = f"💡 *Instant Answer:*\n\n{answer}"
    if topic:
        message += f"\n\n*Topic:* {topic}"
    return message


def get_search_type_keyboard(query: str, current_type: str) -> InlineKeyboardMarkup:
    """Create an inline keyboard for switching search types."""
    keyboard = []
    row = []
    for search_type, label in SEARCH_TYPES.items():
        if search_type == current_type:
            row.append(InlineKeyboardButton(f"✅ {label}", callback_data=f"none"))
        else:
            row.append(
                InlineKeyboardButton(label, callback_data=f"{search_type}:{query}")
            )
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages by performing a web search."""
    query = update.message.text.strip()
    if not query:
        await update.message.reply_text("Please provide a search query.")
        return

    await perform_search(update, context, query, "web")


async def perform_search(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    query: str,
    search_type: str,
) -> None:
    """Perform a search and send results to the user."""
    # Send typing indicator
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    # Perform the search based on type
    if search_type == "web":
        results = await search_web(query)
        message = format_web_results(results)
    elif search_type == "images":
        results = await search_images(query)
        message = format_image_results(results)
    elif search_type == "news":
        results = await search_news(query)
        message = format_news_results(results)
    elif search_type == "answers":
        result = await search_answers(query)
        message = format_answer_result(result)
    else:
        message = "❌ Invalid search type."

    # Add keyboard for switching search types
    keyboard = get_search_type_keyboard(query, search_type)
    reply_markup = keyboard

    # Send the message
    await update.message.reply_text(
        message, parse_mode="Markdown", reply_markup=reply_markup, disable_web_page_preview=True
    )


async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle callback queries from inline keyboards."""
    query = update.callback_query
    await query.answer()

    # Parse the callback data
    data = query.data
    if data == "none":
        return

    search_type, search_query = data.split(":", 1)

    # Perform the new search
    await perform_search(update, context, search_query, search_type)


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /search command."""
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text(
            "Please provide a search query. Example: /search Python programming"
        )
        return
    await perform_search(update, context, query, "web")


async def images_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /images command."""
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text(
            "Please provide a search query. Example: /images cute cats"
        )
        return
    await perform_search(update, context, query, "images")


async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /news command."""
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text(
            "Please provide a search query. Example: /news technology"
        )
        return
    await perform_search(update, context, query, "news")


async def answer_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /answer command."""
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text(
            "Please provide a query. Example: /answer meaning of life"
        )
        return
    await perform_search(update, context, query, "answers")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors that occur during bot operation."""
    logger.error(f"Update {update} caused error {context.error}")
    try:
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ An error occurred while processing your request. Please try again later."
            )
    except Exception as e:
        logger.error(f"Error in error handler: {e}")


def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("images", images_command))
    application.add_handler(CommandHandler("news", news_command))
    application.add_handler(CommandHandler("answer", answer_command))

    # Register message handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Register callback query handler for inline keyboards
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    # Register error handler
    application.add_error_handler(error_handler)

    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()