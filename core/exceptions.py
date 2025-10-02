"""
Custom exceptions for UltraTexto Pro
"""


class UltraTextoException(Exception):
    """Base exception for UltraTexto Pro"""
    pass


class ConfigurationError(UltraTextoException):
    """Raised when there's a configuration error"""
    pass


class FileProcessingError(UltraTextoException):
    """Raised when file processing fails"""
    pass


class ExclusionError(UltraTextoException):
    """Raised when exclusion operations fail"""
    pass


class ExportError(UltraTextoException):
    """Raised when export operations fail"""
    pass


class DirectoryScanError(UltraTextoException):
    """Raised when directory scanning fails"""
    pass


class ThemeError(UltraTextoException):
    """Raised when theme operations fail"""
    pass


class ValidationError(UltraTextoException):
    """Raised when validation fails"""
    pass


class PermissionError(UltraTextoException):
    """Raised when permission is denied"""
    pass


class ResourceNotFoundError(UltraTextoException):
    """Raised when a required resource is not found"""
    pass