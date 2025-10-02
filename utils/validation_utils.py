"""
Validation utility functions for UltraTexto Pro
"""

import re
import os
from pathlib import Path
from typing import Union, List, Optional, Any, Dict
from core.constants import MAX_FILENAME_LENGTH, MAX_PATH_LENGTH


def is_valid_path(path: Union[str, Path]) -> bool:
    """Check if path is valid"""
    try:
        path_obj = Path(path)
        
        # Check path length
        if len(str(path_obj)) > MAX_PATH_LENGTH:
            return False
        
        # Check for invalid characters (Windows)
        invalid_chars = r'[<>"|?*]'
        if re.search(invalid_chars, str(path_obj)):
            return False
        
        # Check for reserved names (Windows)
        reserved_names = {
            'CON', 'PRN', 'AUX', 'NUL',
            'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
            'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
        }
        
        for part in path_obj.parts:
            if part.upper() in reserved_names:
                return False
        
        return True
    except (ValueError, OSError):
        return False


def is_valid_filename(filename: str) -> bool:
    """Check if filename is valid"""
    if not filename or len(filename) > MAX_FILENAME_LENGTH:
        return False
    
    # Check for invalid characters
    invalid_chars = r'[<>:"/\\|?*]'
    if re.search(invalid_chars, filename):
        return False
    
    # Check for reserved names
    reserved_names = {
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }
    
    name_without_ext = filename.rsplit('.', 1)[0] if '.' in filename else filename
    if name_without_ext.upper() in reserved_names:
        return False
    
    # Check for leading/trailing spaces or dots
    if filename.startswith((' ', '.')) or filename.endswith((' ', '.')):
        return False
    
    return True


def is_valid_extension(extension: str) -> bool:
    """Check if file extension is valid"""
    if not extension:
        return False
    
    if not extension.startswith('.'):
        extension = '.' + extension
    
    # Check length
    if len(extension) > 10:
        return False
    
    # Check for invalid characters
    invalid_chars = r'[<>:"/\\|?*\s]'
    if re.search(invalid_chars, extension):
        return False
    
    return True


def is_valid_regex(pattern: str) -> bool:
    """Check if regex pattern is valid"""
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False


def is_valid_size_pattern(pattern: str) -> bool:
    """Check if size pattern is valid (e.g., '>10MB', '<1GB')"""
    size_pattern = r'^[<>=!]+\d+(\.\d+)?(B|KB|MB|GB|TB)$'
    return bool(re.match(size_pattern, pattern.upper()))


def is_valid_email(email: str) -> bool:
    """Check if email is valid"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_url(url: str) -> bool:
    """Check if URL is valid"""
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))


def validate_config_value(key: str, value: Any) -> tuple[bool, str]:
    """Validate configuration value"""
    validations = {
        'ui.window_size': lambda v: (
            isinstance(v, list) and len(v) == 2 and 
            all(isinstance(x, int) and x > 0 for x in v),
            "Window size must be a list of two positive integers"
        ),
        'ui.font_size': lambda v: (
            isinstance(v, int) and 8 <= v <= 72,
            "Font size must be an integer between 8 and 72"
        ),
        'processing.max_file_size_mb': lambda v: (
            isinstance(v, (int, float)) and v > 0,
            "Max file size must be a positive number"
        ),
        'processing.max_workers': lambda v: (
            isinstance(v, int) and 1 <= v <= 16,
            "Max workers must be an integer between 1 and 16"
        ),
        'processing.supported_extensions': lambda v: (
            isinstance(v, list) and all(is_valid_extension(ext) for ext in v),
            "Supported extensions must be a list of valid extensions"
        )
    }
    
    if key in validations:
        is_valid, error_msg = validations[key](value)
        return is_valid, error_msg
    
    return True, ""


def validate_exclusion_rule(rule_type: str, pattern: str) -> tuple[bool, str]:
    """Validate exclusion rule"""
    if not rule_type or not pattern:
        return False, "Rule type and pattern are required"
    
    valid_types = ['file', 'folder', 'extension', 'regex', 'size', 'date']
    if rule_type not in valid_types:
        return False, f"Invalid rule type. Must be one of: {', '.join(valid_types)}"
    
    if rule_type == 'regex':
        if not is_valid_regex(pattern):
            return False, "Invalid regex pattern"
    elif rule_type == 'extension':
        if not is_valid_extension(pattern):
            return False, "Invalid file extension"
    elif rule_type == 'size':
        if not is_valid_size_pattern(pattern):
            return False, "Invalid size pattern (e.g., '>10MB', '<1GB')"
    elif rule_type in ['file', 'folder']:
        if not pattern.strip():
            return False, "Pattern cannot be empty"
    
    return True, ""


def sanitize_input(text: str, max_length: Optional[int] = None) -> str:
    """Sanitize user input"""
    if not isinstance(text, str):
        text = str(text)
    
    # Remove control characters
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\t\n\r')
    
    # Trim whitespace
    text = text.strip()
    
    # Limit length
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text


def validate_json_structure(data: Dict[str, Any], required_keys: List[str]) -> tuple[bool, str]:
    """Validate JSON structure has required keys"""
    if not isinstance(data, dict):
        return False, "Data must be a dictionary"
    
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        return False, f"Missing required keys: {', '.join(missing_keys)}"
    
    return True, ""


def is_safe_path(path: Union[str, Path], base_path: Union[str, Path]) -> bool:
    """Check if path is safe (within base path, no directory traversal)"""
    try:
        path_obj = Path(path).resolve()
        base_obj = Path(base_path).resolve()
        
        # Check if path is within base path
        try:
            path_obj.relative_to(base_obj)
            return True
        except ValueError:
            return False
    except (ValueError, OSError):
        return False


def validate_file_permissions(file_path: Union[str, Path], 
                            read: bool = False, 
                            write: bool = False) -> tuple[bool, str]:
    """Validate file permissions"""
    try:
        path_obj = Path(file_path)
        
        if not path_obj.exists():
            return False, "File does not exist"
        
        if read and not os.access(path_obj, os.R_OK):
            return False, "No read permission"
        
        if write and not os.access(path_obj, os.W_OK):
            return False, "No write permission"
        
        return True, ""
    except (ValueError, OSError) as e:
        return False, str(e)