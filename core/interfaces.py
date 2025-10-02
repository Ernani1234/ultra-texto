"""
Interfaces and abstract base classes for UltraTexto Pro
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Callable, Generator
from pathlib import Path
from datetime import datetime


class IFileProcessor(ABC):
    """Interface for file processing operations"""
    
    @abstractmethod
    def process_files(self, directory: Path, exclusions: List[Any], 
                     progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Process files in a directory"""
        pass
    
    @abstractmethod
    def get_supported_extensions(self) -> List[str]:
        """Get list of supported file extensions"""
        pass


class IExclusionManager(ABC):
    """Interface for exclusion management"""
    
    @abstractmethod
    def add_exclusion(self, rule_type: str, pattern: str, **kwargs) -> bool:
        """Add an exclusion rule"""
        pass
    
    @abstractmethod
    def remove_exclusion(self, rule_id: str) -> bool:
        """Remove an exclusion rule"""
        pass
    
    @abstractmethod
    def should_exclude(self, file_path: Path) -> tuple[bool, str]:
        """Check if a file should be excluded"""
        pass


class IConfigManager(ABC):
    """Interface for configuration management"""
    
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        pass
    
    @abstractmethod
    def save(self) -> bool:
        """Save configuration to file"""
        pass
    
    @abstractmethod
    def load(self) -> bool:
        """Load configuration from file"""
        pass


class IExportManager(ABC):
    """Interface for export operations"""
    
    @abstractmethod
    def export_to_format(self, data: Dict[str, Any], format_type: str, 
                        output_path: Path) -> bool:
        """Export data to specified format"""
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """Get list of supported export formats"""
        pass


class IDirectoryScanner(ABC):
    """Interface for directory scanning operations"""
    
    @abstractmethod
    def scan_directory(self, directory: Path, include_subdirs: bool = True,
                      progress_callback: Optional[Callable] = None) -> Generator:
        """Scan directory and yield file information"""
        pass
    
    @abstractmethod
    def get_directory_stats(self, directory: Path) -> Dict[str, Any]:
        """Get directory statistics"""
        pass


class INotificationManager(ABC):
    """Interface for notification management"""
    
    @abstractmethod
    def show_info(self, message: str, title: str = "Info") -> None:
        """Show info notification"""
        pass
    
    @abstractmethod
    def show_warning(self, message: str, title: str = "Warning") -> None:
        """Show warning notification"""
        pass
    
    @abstractmethod
    def show_error(self, message: str, title: str = "Error") -> None:
        """Show error notification"""
        pass


class IProgressReporter(ABC):
    """Interface for progress reporting"""
    
    @abstractmethod
    def start_progress(self, total: int, description: str = "") -> None:
        """Start progress tracking"""
        pass
    
    @abstractmethod
    def update_progress(self, current: int, message: str = "") -> None:
        """Update progress"""
        pass
    
    @abstractmethod
    def finish_progress(self) -> None:
        """Finish progress tracking"""
        pass


class IThemeManager(ABC):
    """Interface for theme management"""
    
    @abstractmethod
    def apply_theme(self, theme_name: str) -> bool:
        """Apply a theme"""
        pass
    
    @abstractmethod
    def get_available_themes(self) -> List[str]:
        """Get list of available themes"""
        pass
    
    @abstractmethod
    def get_current_theme(self) -> str:
        """Get current theme name"""
        pass