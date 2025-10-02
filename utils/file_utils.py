"""
File utility functions for UltraTexto Pro
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional, Union, Generator
from datetime import datetime
import hashlib


def ensure_directory_exists(directory: Union[str, Path]) -> Path:
    """Ensure a directory exists, create if it doesn't"""
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_file_size_formatted(file_path: Union[str, Path]) -> str:
    """Get formatted file size"""
    try:
        size = Path(file_path).stat().st_size
        return format_file_size(size)
    except (OSError, ValueError):
        return "0 B"


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def get_file_hash(file_path: Union[str, Path], algorithm: str = 'md5') -> Optional[str]:
    """Get file hash"""
    try:
        hash_obj = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except (OSError, ValueError):
        return None


def is_text_file(file_path: Union[str, Path]) -> bool:
    """Check if file is a text file"""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:
                return False
            
        # Try to decode as text
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            f.read(1024)
        return True
    except (OSError, UnicodeDecodeError):
        return False


def safe_copy_file(src: Union[str, Path], dst: Union[str, Path]) -> bool:
    """Safely copy a file"""
    try:
        src_path = Path(src)
        dst_path = Path(dst)
        
        # Ensure destination directory exists
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.copy2(src_path, dst_path)
        return True
    except (OSError, shutil.Error):
        return False


def safe_move_file(src: Union[str, Path], dst: Union[str, Path]) -> bool:
    """Safely move a file"""
    try:
        src_path = Path(src)
        dst_path = Path(dst)
        
        # Ensure destination directory exists
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.move(str(src_path), str(dst_path))
        return True
    except (OSError, shutil.Error):
        return False


def safe_delete_file(file_path: Union[str, Path]) -> bool:
    """Safely delete a file"""
    try:
        Path(file_path).unlink()
        return True
    except (OSError, FileNotFoundError):
        return False


def get_unique_filename(file_path: Union[str, Path]) -> Path:
    """Get a unique filename by adding a counter if file exists"""
    path = Path(file_path)
    if not path.exists():
        return path
    
    counter = 1
    while True:
        new_name = f"{path.stem}_{counter}{path.suffix}"
        new_path = path.parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1


def find_files_by_extension(directory: Union[str, Path], 
                          extensions: List[str],
                          recursive: bool = True) -> Generator[Path, None, None]:
    """Find files by extension"""
    directory = Path(directory)
    extensions = [ext.lower() for ext in extensions]
    
    pattern = "**/*" if recursive else "*"
    
    for file_path in directory.glob(pattern):
        if file_path.is_file() and file_path.suffix.lower() in extensions:
            yield file_path


def get_directory_size(directory: Union[str, Path]) -> int:
    """Get total size of directory"""
    total_size = 0
    directory = Path(directory)
    
    try:
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                try:
                    total_size += file_path.stat().st_size
                except (OSError, ValueError):
                    continue
    except (OSError, ValueError):
        pass
    
    return total_size


def count_files_in_directory(directory: Union[str, Path], 
                           extensions: Optional[List[str]] = None) -> int:
    """Count files in directory"""
    directory = Path(directory)
    count = 0
    
    try:
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                if extensions is None or file_path.suffix.lower() in extensions:
                    count += 1
    except (OSError, ValueError):
        pass
    
    return count


def create_backup(file_path: Union[str, Path], backup_dir: Optional[Union[str, Path]] = None) -> Optional[Path]:
    """Create a backup of a file"""
    try:
        file_path = Path(file_path)
        
        if backup_dir is None:
            backup_dir = file_path.parent / "backups"
        else:
            backup_dir = Path(backup_dir)
        
        ensure_directory_exists(backup_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
        backup_path = backup_dir / backup_name
        
        if safe_copy_file(file_path, backup_path):
            return backup_path
        return None
    except (OSError, ValueError):
        return None


def cleanup_old_backups(backup_dir: Union[str, Path], 
                       max_backups: int = 10,
                       pattern: str = "*") -> int:
    """Clean up old backup files"""
    try:
        backup_dir = Path(backup_dir)
        if not backup_dir.exists():
            return 0
        
        # Get all backup files sorted by modification time
        backup_files = sorted(
            backup_dir.glob(pattern),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        # Remove old backups
        removed_count = 0
        for backup_file in backup_files[max_backups:]:
            if backup_file.is_file():
                try:
                    backup_file.unlink()
                    removed_count += 1
                except OSError:
                    continue
        
        return removed_count
    except (OSError, ValueError):
        return 0