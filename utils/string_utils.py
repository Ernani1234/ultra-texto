"""
String utility functions for UltraTexto Pro
"""

import re
import unicodedata
from typing import List, Optional, Union


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters"""
    # Remove invalid characters for Windows/Linux filenames
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename)
    
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(' .')
    
    # Limit length
    if len(sanitized) > 255:
        name, ext = sanitized.rsplit('.', 1) if '.' in sanitized else (sanitized, '')
        max_name_length = 255 - len(ext) - 1 if ext else 255
        sanitized = name[:max_name_length] + ('.' + ext if ext else '')
    
    return sanitized or 'unnamed'


def normalize_path(path: str) -> str:
    """Normalize path separators"""
    return path.replace('\\', '/').replace('//', '/')


def truncate_string(text: str, max_length: int, suffix: str = '...') -> str:
    """Truncate string with suffix"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def format_duration(seconds: float) -> str:
    """Format duration in human readable format"""
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def format_number(number: Union[int, float], precision: int = 1) -> str:
    """Format number with thousands separator"""
    if isinstance(number, float):
        return f"{number:,.{precision}f}"
    else:
        return f"{number:,}"


def extract_extension(filename: str) -> str:
    """Extract file extension"""
    if '.' not in filename:
        return ''
    return filename.rsplit('.', 1)[1].lower()


def is_valid_regex(pattern: str) -> bool:
    """Check if string is a valid regex pattern"""
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False


def escape_regex(text: str) -> str:
    """Escape special regex characters"""
    return re.escape(text)


def remove_accents(text: str) -> str:
    """Remove accents from text"""
    return ''.join(
        char for char in unicodedata.normalize('NFD', text)
        if unicodedata.category(char) != 'Mn'
    )


def camel_to_snake(name: str) -> str:
    """Convert CamelCase to snake_case"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_to_camel(name: str) -> str:
    """Convert snake_case to CamelCase"""
    components = name.split('_')
    return ''.join(word.capitalize() for word in components)


def pluralize(word: str, count: int) -> str:
    """Simple pluralization"""
    if count == 1:
        return word
    
    # Simple rules for Portuguese
    if word.endswith('ão'):
        return word[:-2] + 'ões'
    elif word.endswith('al'):
        return word[:-2] + 'ais'
    elif word.endswith('el'):
        return word[:-2] + 'éis'
    elif word.endswith('ol'):
        return word[:-2] + 'óis'
    elif word.endswith('ul'):
        return word[:-2] + 'uis'
    elif word.endswith(('a', 'e', 'o')):
        return word + 's'
    else:
        return word + 's'


def highlight_text(text: str, query: str, 
                  start_tag: str = '<mark>', 
                  end_tag: str = '</mark>') -> str:
    """Highlight query in text"""
    if not query:
        return text
    
    # Escape special regex characters in query
    escaped_query = re.escape(query)
    pattern = re.compile(escaped_query, re.IGNORECASE)
    
    return pattern.sub(f'{start_tag}\\g<0>{end_tag}', text)


def clean_whitespace(text: str) -> str:
    """Clean excessive whitespace"""
    # Replace multiple whitespace with single space
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    return text.strip()


def extract_words(text: str) -> List[str]:
    """Extract words from text"""
    return re.findall(r'\b\w+\b', text.lower())


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate simple similarity between two texts"""
    words1 = set(extract_words(text1))
    words2 = set(extract_words(text2))
    
    if not words1 and not words2:
        return 1.0
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union)


def format_list(items: List[str], conjunction: str = 'e') -> str:
    """Format list of items with proper conjunction"""
    if not items:
        return ''
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f'{items[0]} {conjunction} {items[1]}'
    
    return f'{", ".join(items[:-1])} {conjunction} {items[-1]}'


def wrap_text(text: str, width: int = 80) -> List[str]:
    """Wrap text to specified width"""
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + len(current_line) <= width:
            current_line.append(word)
            current_length += len(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines