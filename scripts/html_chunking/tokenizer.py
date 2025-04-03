from typing import Optional, List
from bs4 import BeautifulSoup
import re

# Try to import LlamaIndex settings, but don't fail if it's not available
try:
    from llama_index.core import Settings
    LLAMA_INDEX_AVAILABLE = True
except ImportError:
    LLAMA_INDEX_AVAILABLE = False

def simple_token_count(text: str) -> int:
    """
    A simple tokenization approach that approximates token count for testing.
    
    This is used as a fallback when no embedding model is available.
    
    Args:
        text (str): The text to count tokens for.
        
    Returns:
        int: An approximate token count
    """
    # Split on whitespace and punctuation
    tokens = re.findall(r'\w+|[^\w\s]', text)
    
    # Rough adjustment for subword tokenization
    adjustment_factor = 0.75  # Most tokenizers create fewer tokens than this simple approach
    return int(len(tokens) * adjustment_factor)

def count_tokens(text: str, embed_model=None) -> int:
    """
    Count tokens using the embedding model's tokenizer or fallback to simple counting.
    
    Args:
        text (str): The text to count tokens for.
        embed_model: Optional custom embedding model to use.
    
    Returns:
        int: The number of tokens in the text.
    """
    # Try to use the provided embedding model
    if embed_model is not None:
        try:
            tokenizer = embed_model.tokenizer
            tokens = tokenizer.encode(text)
            return len(tokens)
        except (AttributeError, Exception):
            pass
    
    # Try to use LlamaIndex's default embedding model
    if LLAMA_INDEX_AVAILABLE:
        try:
            embed_model = Settings.embed_model
            tokenizer = embed_model.tokenizer
            tokens = tokenizer.encode(text)
            return len(tokens)
        except (AttributeError, ValueError, Exception):
            pass
    
    # Fallback to simple token counting
    return simple_token_count(text)

def count_html_tokens(html_text: str, count_tag_tokens: bool = True, embed_model=None) -> int:
    """
    Count tokens in HTML text, with option to include or exclude tags.
    
    Args:
        html_text (str): The HTML text to count tokens for.
        count_tag_tokens (bool): Whether to include HTML tags in the token count.
        embed_model: Optional custom embedding model to use.
    
    Returns:
        int: The number of tokens in the HTML text.
    """
    if not count_tag_tokens:
        # Strip HTML tags before counting
        soup = BeautifulSoup(html_text, 'html.parser')
        text = soup.get_text(separator=' ')
        return count_tokens(text, embed_model)
    else:
        # Count tokens including HTML tags
        return count_tokens(html_text, embed_model)
