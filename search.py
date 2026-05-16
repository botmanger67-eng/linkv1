"""
DuckDuckGo search integration module.

Provides functions to search DuckDuckGo for web results, images, news,
and instant answers using the duckduckgo_search library.
"""

from typing import List, Dict, Optional, Any
from duckduckgo_search import DDGS
import logging

# Configure logging
logger = logging.getLogger(__name__)


class DuckDuckGoSearchError(Exception):
    """Custom exception for DuckDuckGo search errors."""
    pass


def search_web(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Search DuckDuckGo for web results.

    Args:
        query: The search query string.
        max_results: Maximum number of results to return (default: 10).

    Returns:
        A list of dictionaries containing web search results.
        Each dictionary contains keys: 'title', 'href', 'body'.

    Raises:
        DuckDuckGoSearchError: If the search fails.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            logger.info(f"Web search for '{query}' returned {len(results)} results")
            return results
    except Exception as e:
        logger.error(f"Web search failed for '{query}': {e}")
        raise DuckDuckGoSearchError(f"Web search failed: {e}")


def search_images(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Search DuckDuckGo for images.

    Args:
        query: The search query string.
        max_results: Maximum number of results to return (default: 10).

    Returns:
        A list of dictionaries containing image search results.
        Each dictionary contains keys: 'title', 'image', 'thumbnail', 'url', 'height', 'width', 'source'.

    Raises:
        DuckDuckGoSearchError: If the search fails.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(query, max_results=max_results))
            logger.info(f"Image search for '{query}' returned {len(results)} results")
            return results
    except Exception as e:
        logger.error(f"Image search failed for '{query}': {e}")
        raise DuckDuckGoSearchError(f"Image search failed: {e}")


def search_news(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Search DuckDuckGo for news.

    Args:
        query: The search query string.
        max_results: Maximum number of results to return (default: 10).

    Returns:
        A list of dictionaries containing news search results.
        Each dictionary contains keys: 'date', 'title', 'body', 'url', 'image', 'source'.

    Raises:
        DuckDuckGoSearchError: If the search fails.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(query, max_results=max_results))
            logger.info(f"News search for '{query}' returned {len(results)} results")
            return results
    except Exception as e:
        logger.error(f"News search failed for '{query}': {e}")
        raise DuckDuckGoSearchError(f"News search failed: {e}")


def search_instant_answer(query: str) -> Optional[Dict[str, Any]]:
    """
    Search DuckDuckGo for an instant answer.

    Args:
        query: The search query string.

    Returns:
        A dictionary containing the instant answer if found, or None if no answer is available.
        The dictionary contains keys: 'abstract', 'abstractText', 'abstractSource', 'image', 
        'heading', 'answer', 'answerType', 'definition', 'definitionSource', 'definitionURL', 
        'entity', 'infobox', 'results', 'type', 'url'.

    Raises:
        DuckDuckGoSearchError: If the search fails.
    """
    try:
        with DDGS() as ddgs:
            result = ddgs.answers(query)
            if result:
                logger.info(f"Instant answer found for '{query}'")
                return result
            else:
                logger.info(f"No instant answer found for '{query}'")
                return None
    except Exception as e:
        logger.error(f"Instant answer search failed for '{query}': {e}")
        raise DuckDuckGoSearchError(f"Instant answer search failed: {e}")


def search_suggestions(query: str, max_results: int = 10) -> List[str]:
    """
    Get search suggestions from DuckDuckGo.

    Args:
        query: The search query string.
        max_results: Maximum number of suggestions to return (default: 10).

    Returns:
        A list of suggestion strings.

    Raises:
        DuckDuckGoSearchError: If the search fails.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.suggestions(query, max_results=max_results))
            suggestions = [item.get('phrase', '') for item in results if item.get('phrase')]
            logger.info(f"Suggestions for '{query}' returned {len(suggestions)} results")
            return suggestions
    except Exception as e:
        logger.error(f"Suggestions search failed for '{query}': {e}")
        raise DuckDuckGoSearchError(f"Suggestions search failed: {e}")


def search_all(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Perform all search types (web, images, news, instant answer) for a given query.

    Args:
        query: The search query string.
        max_results: Maximum number of results per search type (default: 5).

    Returns:
        A dictionary containing results for each search type.
        Keys: 'web', 'images', 'news', 'instant_answer', 'suggestions'.

    Raises:
        DuckDuckGoSearchError: If any search fails.
    """
    results = {}
    try:
        results['web'] = search_web(query, max_results)
        results['images'] = search_images(query, max_results)
        results['news'] = search_news(query, max_results)
        results['instant_answer'] = search_instant_answer(query)
        results['suggestions'] = search_suggestions(query, max_results)
        return results
    except DuckDuckGoSearchError as e:
        logger.error(f"Combined search failed for '{query}': {e}")
        raise DuckDuckGoSearchError(f"Combined search failed: {e}")
