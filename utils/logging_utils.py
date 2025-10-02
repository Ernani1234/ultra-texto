"""
Logging utility functions for UltraTexto Pro
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Union
from datetime import datetime
import traceback


class UltraTextoLogger:
    """Custom logger for UltraTexto Pro"""
    
    def __init__(self, name: str = "UltraTexto", 
                 log_file: Optional[Union[str, Path]] = None,
                 level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (if specified)
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str, *args, **kwargs):
        """Log debug message"""
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        """Log info message"""
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        """Log warning message"""
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        """Log error message"""
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        """Log critical message"""
        self.logger.critical(message, *args, **kwargs)
    
    def exception(self, message: str, *args, **kwargs):
        """Log exception with traceback"""
        self.logger.exception(message, *args, **kwargs)


# Global logger instance
_logger = None


def get_logger(name: str = "UltraTexto", 
               log_file: Optional[Union[str, Path]] = None,
               level: int = logging.INFO) -> UltraTextoLogger:
    """Get or create logger instance"""
    global _logger
    if _logger is None:
        _logger = UltraTextoLogger(name, log_file, level)
    return _logger


def log_function_call(func):
    """Decorator to log function calls"""
    def wrapper(*args, **kwargs):
        logger = get_logger()
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed with error: {str(e)}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            raise
    
    return wrapper


def log_performance(func):
    """Decorator to log function performance"""
    def wrapper(*args, **kwargs):
        import time
        logger = get_logger()
        
        start_time = time.time()
        logger.debug(f"Starting {func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time
            logger.debug(f"{func.__name__} completed in {duration:.3f}s")
            return result
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            logger.error(f"{func.__name__} failed after {duration:.3f}s: {str(e)}")
            raise
    
    return wrapper


def log_exception(exception: Exception, context: str = ""):
    """Log exception with context"""
    logger = get_logger()
    
    error_msg = f"Exception in {context}: {str(exception)}" if context else str(exception)
    logger.error(error_msg)
    logger.debug(f"Traceback: {traceback.format_exc()}")


def log_system_info():
    """Log system information"""
    import platform
    import psutil
    
    logger = get_logger()
    
    logger.info("=== System Information ===")
    logger.info(f"Platform: {platform.platform()}")
    logger.info(f"Python: {platform.python_version()}")
    logger.info(f"Architecture: {platform.architecture()[0]}")
    logger.info(f"Processor: {platform.processor()}")
    logger.info(f"Memory: {psutil.virtual_memory().total / (1024**3):.1f} GB")
    logger.info(f"CPU Cores: {psutil.cpu_count()}")
    logger.info("========================")


def create_debug_report(error: Exception, context: dict = None) -> str:
    """Create detailed debug report"""
    import platform
    import sys
    
    report_lines = [
        "=== UltraTexto Pro Debug Report ===",
        f"Timestamp: {datetime.now().isoformat()}",
        f"Error: {type(error).__name__}: {str(error)}",
        "",
        "=== System Information ===",
        f"Platform: {platform.platform()}",
        f"Python: {platform.python_version()}",
        f"Architecture: {platform.architecture()[0]}",
        "",
        "=== Context Information ===",
    ]
    
    if context:
        for key, value in context.items():
            report_lines.append(f"{key}: {value}")
    
    report_lines.extend([
        "",
        "=== Traceback ===",
        traceback.format_exc(),
        "",
        "=== End Report ==="
    ])
    
    return "\n".join(report_lines)


def save_debug_report(error: Exception, 
                     context: dict = None,
                     output_dir: Union[str, Path] = "logs") -> Optional[Path]:
    """Save debug report to file"""
    try:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = output_path / f"debug_report_{timestamp}.txt"
        
        report_content = create_debug_report(error, context)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return report_file
    except Exception as e:
        logger = get_logger()
        logger.error(f"Failed to save debug report: {str(e)}")
        return None


class ProgressLogger:
    """Logger for progress tracking"""
    
    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = datetime.now()
        self.logger = get_logger()
        
        self.logger.info(f"Starting {description} - Total: {total}")
    
    def update(self, increment: int = 1, message: str = ""):
        """Update progress"""
        self.current += increment
        percentage = (self.current / self.total) * 100 if self.total > 0 else 0
        
        elapsed = datetime.now() - self.start_time
        
        log_message = f"{self.description}: {self.current}/{self.total} ({percentage:.1f}%)"
        if message:
            log_message += f" - {message}"
        
        self.logger.debug(log_message)
        
        # Log milestone percentages
        if percentage in [25, 50, 75, 100]:
            self.logger.info(f"{self.description}: {percentage:.0f}% complete")
    
    def finish(self, message: str = ""):
        """Finish progress tracking"""
        elapsed = datetime.now() - self.start_time
        
        final_message = f"{self.description} completed in {elapsed.total_seconds():.2f}s"
        if message:
            final_message += f" - {message}"
        
        self.logger.info(final_message)