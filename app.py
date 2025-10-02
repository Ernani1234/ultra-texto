"""
UltraTexto Pro - Main Application Entry Point
Versão 2.0 - Arquitetura Modular Aprimorada
"""

import sys
import os
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Core imports
from core.constants import APP_NAME, APP_VERSION, APP_DESCRIPTION
from core.exceptions import UltraTextoException
from utils.logging_utils import get_logger, log_system_info, log_exception

# Application imports
from ui.main_window import MainWindow
from services.application_service import ApplicationService


class UltraTextoApp:
    """Main application class with improved architecture"""
    
    def __init__(self):
        self.logger = get_logger("UltraTextoApp")
        self.app_service = None
        self.main_window = None
        
    def initialize(self) -> bool:
        """Initialize the application"""
        try:
            self.logger.info(f"Initializing {APP_NAME} v{APP_VERSION}")
            log_system_info()
            
            # Initialize application service
            self.app_service = ApplicationService()
            if not self.app_service.initialize():
                self.logger.error("Failed to initialize application service")
                return False
            
            # Initialize main window
            self.main_window = MainWindow(self.app_service)
            if not self.main_window.initialize():
                self.logger.error("Failed to initialize main window")
                return False
            
            self.logger.info("Application initialized successfully")
            return True
            
        except Exception as e:
            log_exception(e, "Application initialization")
            return False
    
    def run(self):
        """Run the application"""
        try:
            if not self.initialize():
                self.logger.critical("Failed to initialize application")
                return 1
            
            self.logger.info("Starting application main loop")
            self.main_window.run()
            
            self.logger.info("Application closed normally")
            return 0
            
        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user")
            return 0
        except Exception as e:
            log_exception(e, "Application runtime")
            return 1
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            self.logger.info("Cleaning up application resources")
            
            if self.main_window:
                self.main_window.cleanup()
            
            if self.app_service:
                self.app_service.cleanup()
                
        except Exception as e:
            log_exception(e, "Application cleanup")


def main():
    """Main entry point"""
    app = UltraTextoApp()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())