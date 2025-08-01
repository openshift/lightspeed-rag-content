"""
Tokenizer module for HTML content.
"""

from typing import Optional, Union, Callable
from bs4 import BeautifulSoup
import re
import sys
import warnings

# Import LlamaIndex/HuggingFace dependencies
# These are required, not optional
try:
    from llama_index.core import Settings as LlamaIndexSettings
except ImportError:
    raise ImportError("LlamaIndex is required for token counting. Install with 'pip install llama-index'")

try:
    from transformers import AutoTokenizer
except ImportError:
    raise ImportError("HuggingFace transformers is required for token counting. Install with 'pip install transformers'")

# Constants
MAX_CHUNK_SIZE = 5000
WORDS_PER_BATCH = 100


class TokenCounter:
    """
    A class that counts tokens in text using LlamaIndex or HuggingFace tokenizers.
    """
    
    def __init__(self, custom_tokenizer: Optional[Callable[[str], list[str]]] = None) -> None:
        """
        Initialize the TokenCounter.
        
        Args:
            custom_tokenizer: An optional custom tokenizer function that takes a string
                             and returns a list of tokens.
        """
        self.tokenizer = custom_tokenizer
        self.hf_tokenizer = None
        self._initialize_tokenizer()
    
    def _initialize_tokenizer(self) -> None:
        """Initialize the tokenizer."""
        if self.tokenizer is not None:
            return
            
        try:
            embed_model = LlamaIndexSettings.embed_model
            if hasattr(embed_model, 'tokenizer'):
                self.tokenizer = lambda text: embed_model.tokenizer.encode(text)
                return
        except (AttributeError, ValueError, ImportError, RuntimeError):
            pass
        
        try:
            self.hf_tokenizer = AutoTokenizer.from_pretrained("gpt2")
            self.tokenizer = lambda text: self.hf_tokenizer.encode(text, add_special_tokens=False)
            return
        except (AttributeError, ValueError, ImportError, RuntimeError):
            pass
        
        raise RuntimeError(
            "Failed to initialize a tokenizer. Either provide a custom tokenizer, "
            "configure LlamaIndex Settings.embed_model with a tokenizer, "
            "or ensure HuggingFace transformers is properly installed."
        )
    
    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in the text.
        
        Args:
            text: The text to count tokens for.
        
        Returns:
            The number of tokens in the text.
        """
        if not text:
            return 0

        try:
            if len(text) > MAX_CHUNK_SIZE:
                chunks = [text[i:i+MAX_CHUNK_SIZE] for i in range(0, len(text), MAX_CHUNK_SIZE)]
                token_count = 0
                for chunk in chunks:
                    tokens = self.tokenizer(chunk)
                    token_count += len(tokens)
                return token_count
            else:
                tokens = self.tokenizer(text)
                return len(tokens)
        except Exception as e:
            if "sequence length is longer than the specified maximum" in str(e) and self.hf_tokenizer is not None:
                warnings.warn(f"Token counting using full text failed: {e}. Using manual chunking approach.")
                words = re.findall(r'\b\w+\b|[^\w\s]', text)
                chunks = [' '.join(words[i:i+WORDS_PER_BATCH]) for i in range(0, len(words), WORDS_PER_BATCH)]
                token_count = 0
                for chunk in chunks:
                    try:
                        tokens = self.hf_tokenizer.encode(chunk, add_special_tokens=False)
                        token_count += len(tokens)
                    except Exception:
                        token_count += len(chunk.split())
                return token_count
            else:
                raise
    
    def count_html_tokens(self, html_text: str, count_tag_tokens: bool = True) -> int:
        """
        Count tokens in HTML text, with option to include or exclude tags.
        
        Args:
            html_text: The HTML text to count tokens for.
            count_tag_tokens: Whether to include HTML tags in the token count.
        
        Returns:
            The number of tokens in the HTML text.
        """
        if not html_text:
            return 0
            
        try:
            if not count_tag_tokens:
                soup = BeautifulSoup(html_text, 'html.parser')
                text = soup.get_text(separator=' ')
                return self.count_tokens(text)
            else:
                return self.count_tokens(html_text)
        except Exception as e:
            if not count_tag_tokens:
                text = re.sub(r'<[^>]+>', ' ', html_text)
                return len(text.split())
            else:
                return len(html_text.split())


# Create a singleton instance for convenience
token_counter = TokenCounter()


def count_tokens(text: str) -> int:
    """
    Count tokens in text using the global TokenCounter instance.
    
    Args:
        text: The text to count tokens for.
    
    Returns:
        The number of tokens in the text.
    """
    return token_counter.count_tokens(text)


def count_html_tokens(html_text: str, count_tag_tokens: bool = True) -> int:
    """
    Count tokens in HTML text using the global TokenCounter instance.
    
    Args:
        html_text: The HTML text to count tokens for.
        count_tag_tokens: Whether to include HTML tags in the token count.
    
    Returns:
        The number of tokens in the HTML text.
    """
    return token_counter.count_html_tokens(html_text, count_tag_tokens)


def set_custom_tokenizer(tokenizer_func: Callable[[str], list[str]]) -> None:
    """
    Set a custom tokenizer function for the global TokenCounter instance.
    
    Args:
        tokenizer_func: A function that takes a string and returns a list of tokens.
    """
    global token_counter
    token_counter = TokenCounter(tokenizer_func)
