"""
Main application service for UltraTexto Pro
Coordinates all other services and manages application state
"""

from typing import Optional, Dict, Any
from pathlib import Path

from core.interfaces import (
    IConfigManager, IFileProcessor, IExclusionManager, 
    IExportManager, IDirectoryScanner, INotificationManager
)
from core.exceptions import UltraTextoException
from utils.logging_utils import get_logger, log_exception

from modules.config_manager import ConfigManager
from modules.file_processor import FileProcessor
from modules.exclusion_manager import ExclusionManager
from modules.export_manager import ExportManager
from modules.directory_scanner import DirectoryScanner

from .config_service import ConfigService
from .file_service import FileService
from .export_service import ExportService
from .theme_service import ThemeService


class ApplicationService:
    """Main application service that coordinates all other services"""
    
    def __init__(self):
        self.logger = get_logger("ApplicationService")
        
        # Core managers
        self._config_manager: Optional[IConfigManager] = None
        self._file_processor: Optional[IFileProcessor] = None
        self._exclusion_manager: Optional[IExclusionManager] = None
        self._export_manager: Optional[IExportManager] = None
        self._directory_scanner: Optional[IDirectoryScanner] = None
        
        # Services
        self._config_service: Optional[ConfigService] = None
        self._file_service: Optional[FileService] = None
        self._export_service: Optional[ExportService] = None
        self._theme_service: Optional[ThemeService] = None
        
        # Application state
        self._current_directory: Optional[Path] = None
        self._processing_stats: Optional[Dict[str, Any]] = None
        self._is_initialized = False
    
    def initialize(self) -> bool:
        """Initialize all services and managers"""
        try:
            self.logger.info("Initializing application service")
            
            # Initialize core managers
            self._config_manager = ConfigManager()
            self._file_processor = FileProcessor()
            self._exclusion_manager = ExclusionManager()
            self._export_manager = ExportManager()
            self._directory_scanner = DirectoryScanner()
            
            # Initialize services
            self._config_service = ConfigService(self._config_manager)
            self._file_service = FileService(
                self._file_processor, 
                self._directory_scanner,
                self._exclusion_manager
            )
            self._export_service = ExportService(self._export_manager)
            self._theme_service = ThemeService(self._config_manager)
            
            # Load initial configuration
            if not self._config_service.load_config():
                self.logger.warning("Failed to load configuration, using defaults")
            
            # Apply auto exclusions
            self._exclusion_manager.apply_auto_exclusions(self._config_manager)
            
            self._is_initialized = True
            self.logger.info("Application service initialized successfully")
            return True
            
        except Exception as e:
            log_exception(e, "ApplicationService.initialize")
            return False
    
    def cleanup(self):
        """Cleanup all services"""
        try:
            self.logger.info("Cleaning up application service")
            
            # Save configuration before cleanup
            if self._config_service:
                self._config_service.save_config()
            
            # Cleanup services
            services = [
                self._theme_service,
                self._export_service,
                self._file_service,
                self._config_service
            ]
            
            for service in services:
                if service and hasattr(service, 'cleanup'):
                    try:
                        service.cleanup()
                    except Exception as e:
                        log_exception(e, f"Cleanup {service.__class__.__name__}")
            
            self._is_initialized = False
            
        except Exception as e:
            log_exception(e, "ApplicationService.cleanup")
    
    # Properties for accessing services
    @property
    def config_service(self) -> ConfigService:
        """Get configuration service"""
        if not self._is_initialized:
            raise UltraTextoException("Application service not initialized")
        return self._config_service
    
    @property
    def file_service(self) -> FileService:
        """Get file service"""
        if not self._is_initialized:
            raise UltraTextoException("Application service not initialized")
        return self._file_service
    
    @property
    def export_service(self) -> ExportService:
        """Get export service"""
        if not self._is_initialized:
            raise UltraTextoException("Application service not initialized")
        return self._export_service
    
    @property
    def theme_service(self) -> ThemeService:
        """Get theme service"""
        if not self._is_initialized:
            raise UltraTextoException("Application service not initialized")
        return self._theme_service
    
    # Properties for accessing core managers
    @property
    def config_manager(self) -> IConfigManager:
        """Get configuration manager"""
        if not self._is_initialized:
            raise UltraTextoException("Application service not initialized")
        return self._config_manager
    
    @property
    def exclusion_manager(self) -> IExclusionManager:
        """Get exclusion manager"""
        if not self._is_initialized:
            raise UltraTextoException("Application service not initialized")
        return self._exclusion_manager
    
    # Application state management
    @property
    def current_directory(self) -> Optional[Path]:
        """Get current directory"""
        return self._current_directory
    
    @current_directory.setter
    def current_directory(self, directory: Optional[Path]):
        """Set current directory"""
        self._current_directory = directory
        if directory:
            self.logger.info(f"Current directory set to: {directory}")
    
    @property
    def processing_stats(self) -> Optional[Dict[str, Any]]:
        """Get processing statistics"""
        return self._processing_stats
    
    @processing_stats.setter
    def processing_stats(self, stats: Optional[Dict[str, Any]]):
        """Set processing statistics"""
        self._processing_stats = stats
    
    @property
    def is_initialized(self) -> bool:
        """Check if service is initialized"""
        return self._is_initialized
    
    def get_supported_extensions(self) -> list[str]:
        """Get supported file extensions"""
        return self._file_service.get_supported_extensions()
    
    def get_supported_export_formats(self) -> list[str]:
        """Get supported export formats"""
        return self._export_service.get_supported_formats()
    
    def get_available_themes(self) -> list[str]:
        """Get available themes"""
        return self._theme_service.get_available_themes()
    
    def get_application_info(self) -> Dict[str, Any]:
        """Get application information"""
        from core.constants import APP_NAME, APP_VERSION, APP_DESCRIPTION
        
        return {
            'name': APP_NAME,
            'version': APP_VERSION,
            'description': APP_DESCRIPTION,
            'initialized': self._is_initialized,
            'current_directory': str(self._current_directory) if self._current_directory else None,
            'supported_extensions': len(self.get_supported_extensions()),
            'supported_formats': len(self.get_supported_export_formats()),
            'available_themes': len(self.get_available_themes())
        }