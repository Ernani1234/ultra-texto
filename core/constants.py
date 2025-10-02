"""
Constants for UltraTexto Pro
"""

from pathlib import Path

# Application Information
APP_NAME = "UltraTexto Pro"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "Ferramenta Avançada de Processamento de Arquivos"
APP_AUTHOR = "UltraTexto Pro Team"

# File Extensions
DEFAULT_SUPPORTED_EXTENSIONS = {
    '.js', '.php', '.vue', '.cs', '.py', '.java', '.ts', '.cy',
    '.json', '.cshtml', '.html', '.csv', '.txt', '.md', '.xml',
    '.css', '.scss', '.sass', '.jsx', '.tsx', '.cpp', '.c', '.h',
    '.go', '.rs', '.rb', '.swift', '.kt', '.dart', '.scala'
}

# UI Constants
DEFAULT_WINDOW_SIZE = (1200, 800)
MIN_WINDOW_SIZE = (1000, 600)
DEFAULT_FONT_FAMILY = "Segoe UI"
DEFAULT_FONT_SIZE = 10

# Processing Constants
DEFAULT_MAX_FILE_SIZE_MB = 10
DEFAULT_CHUNK_SIZE = 1024
DEFAULT_MAX_WORKERS = 4
DEFAULT_ENCODING_FALLBACKS = ["utf-8", "latin-1", "cp1252", "iso-8859-1"]

# Directory Constants
CONFIG_DIR = "config"
OUTPUT_DIR = "output"
TEMPLATES_DIR = "templates"
THEMES_DIR = "themes"
BACKUPS_DIR = "backups"

# File Names
CONFIG_FILE = "settings.json"
HISTORY_FILE = "history.json"
EXCLUSION_PROFILES_FILE = "exclusion_profiles.json"

# Export Formats
SUPPORTED_EXPORT_FORMATS = {
    'txt': 'Plain Text',
    'json': 'JSON',
    'xml': 'XML',
    'csv': 'CSV',
    'html': 'HTML Report'
}

# Theme Names
AVAILABLE_THEMES = ['dark', 'light', 'auto']

# Processing Modes
PROCESSING_MODES = {
    'content': 'Conteúdo dos Arquivos',
    'structure': 'Estrutura de Diretórios',
    'both': 'Ambos'
}

# Exclusion Rule Types
EXCLUSION_RULE_TYPES = {
    'file': 'Arquivo Específico',
    'folder': 'Pasta',
    'extension': 'Extensão',
    'regex': 'Expressão Regular',
    'size': 'Tamanho',
    'date': 'Data de Modificação'
}

# Default Exclusions
DEFAULT_EXCLUSIONS = [
    {'rule_type': 'folder', 'pattern': '__pycache__', 'description': 'Python cache'},
    {'rule_type': 'folder', 'pattern': '.git', 'description': 'Git repository'},
    {'rule_type': 'folder', 'pattern': 'node_modules', 'description': 'Node.js modules'},
    {'rule_type': 'folder', 'pattern': '.vscode', 'description': 'VS Code settings'},
    {'rule_type': 'folder', 'pattern': '.idea', 'description': 'IntelliJ IDEA settings'},
    {'rule_type': 'extension', 'pattern': '.pyc', 'description': 'Python compiled'},
    {'rule_type': 'extension', 'pattern': '.pyo', 'description': 'Python optimized'},
    {'rule_type': 'extension', 'pattern': '.exe', 'description': 'Executable files'},
    {'rule_type': 'extension', 'pattern': '.dll', 'description': 'Dynamic libraries'},
    {'rule_type': 'extension', 'pattern': '.so', 'description': 'Shared objects'},
]

# Progress Messages
PROGRESS_MESSAGES = {
    'scanning': 'Escaneando diretório...',
    'processing': 'Processando arquivos...',
    'exporting': 'Exportando resultados...',
    'saving': 'Salvando configurações...',
    'loading': 'Carregando configurações...',
    'analyzing': 'Analisando arquivos...',
    'filtering': 'Aplicando filtros...',
    'generating': 'Gerando relatório...'
}

# Status Messages
STATUS_MESSAGES = {
    'ready': 'Pronto',
    'scanning': 'Escaneando...',
    'processing': 'Processando...',
    'completed': 'Concluído',
    'error': 'Erro',
    'cancelled': 'Cancelado'
}

# Color Schemes
DARK_THEME_COLORS = {
    'bg': '#2b2b2b',
    'fg': '#ffffff',
    'select_bg': '#404040',
    'select_fg': '#ffffff',
    'button_bg': '#404040',
    'button_fg': '#ffffff',
    'entry_bg': '#404040',
    'entry_fg': '#ffffff',
    'frame_bg': '#2b2b2b',
    'accent': '#0078d4',
    'success': '#107c10',
    'warning': '#ff8c00',
    'error': '#d13438'
}

# Validation Rules
MAX_FILENAME_LENGTH = 255
MAX_PATH_LENGTH = 4096
MAX_EXCLUSION_RULES = 1000
MAX_RECENT_DIRECTORIES = 20