"""
Módulo de gerenciamento de configurações para UltraTexto Pro
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import shutil

class ConfigManager:
    """Gerenciador de configurações da aplicação"""
    
    DEFAULT_CONFIG = {
        "version": "2.0.0",
        "ui": {
            "theme": "dark",
            "window_size": [1200, 800],
            "window_position": "center",
            "auto_save_layout": True,
            "show_tooltips": True,
            "animation_enabled": True,
            "font_family": "Segoe UI",
            "font_size": 10
        },
        "processing": {
            "supported_extensions": [
                ".js", ".php", ".vue", ".cs", ".py", ".java", ".ts", ".cy",
                ".json", ".cshtml", ".html", ".csv", ".txt", ".md", ".xml",
                ".css", ".scss", ".sass", ".jsx", ".tsx", ".cpp", ".c", ".h"
            ],
            "include_subdirectories": True,
            "include_files_in_structure": True,
            "processing_mode": "content",
            "max_file_size_mb": 10,
            "encoding_fallbacks": ["utf-8", "latin-1", "cp1252", "iso-8859-1"],
            "chunk_size": 1024,
            "parallel_processing": True,
            "max_workers": 4
        },
        "output": {
            "auto_open_results": True,
            "create_backup": False,
            "compress_output": False,
            "output_directory": "output",
            "filename_template": "arquivo_{counter}",
            "structure_filename_template": "estrutura_{counter}",
            "timestamp_in_filename": True,
            "max_output_files": 100
        },
        "exclusions": {
            "current_profile": "Padrão",
            "auto_exclude_common": True,
            "case_sensitive": False,
            "use_regex": True
        },
        "export": {
            "default_format": "text",
            "include_statistics": True,
            "include_metadata": True,
            "html_theme": "dark",
            "json_pretty_print": True,
            "xml_formatted": True
        },
        "advanced": {
            "enable_logging": True,
            "log_level": "INFO",
            "max_log_files": 10,
            "cache_enabled": True,
            "cache_size_mb": 100,
            "auto_cleanup": True,
            "cleanup_days": 30,
            "performance_monitoring": False
        },
        "shortcuts": {
            "process_files": "Ctrl+P",
            "select_directory": "Ctrl+O",
            "clear_all": "Ctrl+Shift+C",
            "open_results": "Ctrl+R",
            "export_results": "Ctrl+E",
            "toggle_exclusions": "Ctrl+X",
            "search": "Ctrl+F",
            "settings": "Ctrl+,",
            "quit": "Ctrl+Q"
        },
        "history": {
            "max_recent_directories": 10,
            "max_recent_files": 20,
            "save_processing_history": True,
            "auto_load_last_directory": False
        }
    }
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
        self.config_file = self.config_dir / "settings.json"
        self.backup_dir = self.config_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        self.config = self.DEFAULT_CONFIG.copy()
        self.load_config()
        
        # Histórico
        self.recent_directories = []
        self.recent_files = []
        self.processing_history = []
        
        self.load_history()
    
    def load_config(self):
        """Carrega configurações do arquivo"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                
                # Mesclar com configurações padrão
                self.config = self._merge_configs(self.DEFAULT_CONFIG, saved_config)
                
                # Validar configurações
                self._validate_config()
            else:
                # Criar arquivo de configuração padrão
                self.save_config()
        
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
            self.config = self.DEFAULT_CONFIG.copy()
    
    def save_config(self):
        """Salva configurações no arquivo"""
        try:
            # Criar backup antes de salvar
            self._create_backup()
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
    
    def _merge_configs(self, default: Dict, saved: Dict) -> Dict:
        """Mescla configurações salvas com padrões"""
        result = default.copy()
        
        for key, value in saved.items():
            if key in result:
                if isinstance(value, dict) and isinstance(result[key], dict):
                    result[key] = self._merge_configs(result[key], value)
                else:
                    result[key] = value
            else:
                result[key] = value
        
        return result
    
    def _validate_config(self):
        """Valida configurações carregadas"""
        # Validar extensões suportadas
        extensions = self.config["processing"]["supported_extensions"]
        if not isinstance(extensions, list):
            self.config["processing"]["supported_extensions"] = self.DEFAULT_CONFIG["processing"]["supported_extensions"]
        
        # Validar tamanhos
        if self.config["processing"]["max_file_size_mb"] <= 0:
            self.config["processing"]["max_file_size_mb"] = 10
        
        if self.config["processing"]["max_workers"] <= 0:
            self.config["processing"]["max_workers"] = 4
        
        # Validar diretórios
        output_dir = self.config["output"]["output_directory"]
        if not output_dir or not isinstance(output_dir, str):
            self.config["output"]["output_directory"] = "output"
    
    def _create_backup(self):
        """Cria backup da configuração atual"""
        if self.config_file.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"settings_backup_{timestamp}.json"
            
            try:
                shutil.copy2(self.config_file, backup_file)
                
                # Limitar número de backups
                self._cleanup_backups()
            
            except Exception as e:
                print(f"Erro ao criar backup: {e}")
    
    def _cleanup_backups(self, max_backups: int = 10):
        """Remove backups antigos"""
        try:
            backup_files = list(self.backup_dir.glob("settings_backup_*.json"))
            backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Remover backups excedentes
            for backup_file in backup_files[max_backups:]:
                backup_file.unlink()
        
        except Exception as e:
            print(f"Erro ao limpar backups: {e}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Obtém valor de configuração usando caminho com pontos"""
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any):
        """Define valor de configuração usando caminho com pontos"""
        keys = key_path.split('.')
        config = self.config
        
        # Navegar até o penúltimo nível
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Definir valor
        config[keys[-1]] = value
    
    def reset_to_defaults(self):
        """Reseta configurações para padrões"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save_config()
    
    def export_config(self, file_path: str):
        """Exporta configurações para arquivo"""
        export_data = {
            "config": self.config,
            "recent_directories": self.recent_directories,
            "recent_files": self.recent_files,
            "processing_history": self.processing_history,
            "exported_at": datetime.now().isoformat(),
            "version": self.config["version"]
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    def import_config(self, file_path: str):
        """Importa configurações de arquivo"""
        with open(file_path, 'r', encoding='utf-8') as f:
            import_data = json.load(f)
        
        # Validar versão
        imported_version = import_data.get("version", "1.0.0")
        if imported_version != self.config["version"]:
            print(f"Aviso: Importando configurações de versão diferente ({imported_version})")
        
        # Importar configurações
        if "config" in import_data:
            self.config = self._merge_configs(self.DEFAULT_CONFIG, import_data["config"])
        
        # Importar histórico
        if "recent_directories" in import_data:
            self.recent_directories = import_data["recent_directories"]
        
        if "recent_files" in import_data:
            self.recent_files = import_data["recent_files"]
        
        if "processing_history" in import_data:
            self.processing_history = import_data["processing_history"]
        
        # Salvar configurações importadas
        self.save_config()
        self.save_history()
    
    def add_recent_directory(self, directory: str):
        """Adiciona diretório ao histórico recente"""
        directory = str(Path(directory).resolve())
        
        # Remover se já existe
        if directory in self.recent_directories:
            self.recent_directories.remove(directory)
        
        # Adicionar no início
        self.recent_directories.insert(0, directory)
        
        # Limitar tamanho
        max_recent = self.get("history.max_recent_directories", 10)
        self.recent_directories = self.recent_directories[:max_recent]
        
        self.save_history()
    
    def add_recent_file(self, file_path: str):
        """Adiciona arquivo ao histórico recente"""
        file_path = str(Path(file_path).resolve())
        
        # Remover se já existe
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        
        # Adicionar no início
        self.recent_files.insert(0, file_path)
        
        # Limitar tamanho
        max_recent = self.get("history.max_recent_files", 20)
        self.recent_files = self.recent_files[:max_recent]
        
        self.save_history()
    
    def add_processing_entry(self, entry: Dict):
        """Adiciona entrada ao histórico de processamento"""
        if not self.get("history.save_processing_history", True):
            return
        
        entry["timestamp"] = datetime.now().isoformat()
        
        # Adicionar no início
        self.processing_history.insert(0, entry)
        
        # Limitar tamanho
        max_history = 100
        self.processing_history = self.processing_history[:max_history]
        
        self.save_history()
    
    def get_recent_directories(self) -> List[str]:
        """Retorna diretórios recentes válidos"""
        valid_dirs = []
        for directory in self.recent_directories:
            if Path(directory).exists():
                valid_dirs.append(directory)
        
        # Atualizar lista se mudou
        if len(valid_dirs) != len(self.recent_directories):
            self.recent_directories = valid_dirs
            self.save_history()
        
        return valid_dirs
    
    def get_recent_files(self) -> List[str]:
        """Retorna arquivos recentes válidos"""
        valid_files = []
        for file_path in self.recent_files:
            if Path(file_path).exists():
                valid_files.append(file_path)
        
        # Atualizar lista se mudou
        if len(valid_files) != len(self.recent_files):
            self.recent_files = valid_files
            self.save_history()
        
        return valid_files
    
    def load_history(self):
        """Carrega histórico do arquivo"""
        history_file = self.config_dir / "history.json"
        
        try:
            if history_file.exists():
                with open(history_file, 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
                
                self.recent_directories = history_data.get("recent_directories", [])
                self.recent_files = history_data.get("recent_files", [])
                self.processing_history = history_data.get("processing_history", [])
        
        except Exception as e:
            print(f"Erro ao carregar histórico: {e}")
    
    def save_history(self):
        """Salva histórico no arquivo"""
        history_file = self.config_dir / "history.json"
        
        try:
            history_data = {
                "recent_directories": self.recent_directories,
                "recent_files": self.recent_files,
                "processing_history": self.processing_history,
                "last_updated": datetime.now().isoformat()
            }
            
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            print(f"Erro ao salvar histórico: {e}")
    
    def clear_history(self):
        """Limpa todo o histórico"""
        self.recent_directories = []
        self.recent_files = []
        self.processing_history = []
        self.save_history()
    
    def get_supported_extensions(self) -> List[str]:
        """Retorna lista de extensões suportadas"""
        return self.get("processing.supported_extensions", [])
    
    def set_supported_extensions(self, extensions: List[str]):
        """Define extensões suportadas"""
        # Normalizar extensões
        normalized = []
        for ext in extensions:
            ext = ext.strip().lower()
            if not ext.startswith('.'):
                ext = '.' + ext
            normalized.append(ext)
        
        self.set("processing.supported_extensions", normalized)
        self.save_config()
    
    def get_output_directory(self) -> Path:
        """Retorna diretório de saída"""
        output_dir = Path(self.get("output.output_directory", "output"))
        output_dir.mkdir(exist_ok=True)
        return output_dir
    
    def get_next_filename(self, base_template: str, extension: str = ".txt") -> str:
        """Gera próximo nome de arquivo disponível"""
        output_dir = self.get_output_directory()
        
        # Adicionar timestamp se configurado
        if self.get("output.timestamp_in_filename", True):
            timestamp = datetime.now().strftime("_%Y%m%d_%H%M%S")
            template = base_template + timestamp
        else:
            template = base_template
        
        # Procurar próximo número disponível
        counter = 1
        while True:
            filename = template.replace("{counter}", str(counter)) + extension
            file_path = output_dir / filename
            
            if not file_path.exists():
                return str(file_path)
            
            counter += 1
            
            # Evitar loop infinito
            if counter > 10000:
                filename = template.replace("{counter}", str(int(time.time()))) + extension
                return str(output_dir / filename)
    
    def cleanup_old_files(self):
        """Remove arquivos antigos baseado na configuração"""
        if not self.get("advanced.auto_cleanup", True):
            return
        
        cleanup_days = self.get("advanced.cleanup_days", 30)
        output_dir = self.get_output_directory()
        
        try:
            cutoff_time = datetime.now().timestamp() - (cleanup_days * 24 * 60 * 60)
            
            for file_path in output_dir.iterdir():
                if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    print(f"Arquivo removido: {file_path}")
        
        except Exception as e:
            print(f"Erro na limpeza automática: {e}")
    
    def get_theme_colors(self) -> Dict[str, str]:
        """Retorna cores do tema atual"""
        # Importar cores do tema escuro
        try:
            from themes.dark_theme import DarkTheme
            return DarkTheme.COLORS
        except ImportError:
            # Cores padrão se não conseguir importar
            return {
                'bg_primary': '#1e1e1e',
                'bg_secondary': '#2d2d2d',
                'text_primary': '#ffffff',
                'accent_primary': '#14a085'
            }
    
    def validate_and_fix_config(self):
        """Valida e corrige configurações inconsistentes"""
        changes_made = False
        
        # Verificar se diretório de saída existe
        output_dir = self.get("output.output_directory", "output")
        if not Path(output_dir).exists():
            try:
                Path(output_dir).mkdir(parents=True, exist_ok=True)
            except:
                self.set("output.output_directory", "output")
                changes_made = True
        
        # Verificar extensões suportadas
        extensions = self.get("processing.supported_extensions", [])
        if not extensions:
            self.set("processing.supported_extensions", self.DEFAULT_CONFIG["processing"]["supported_extensions"])
            changes_made = True
        
        # Verificar valores numéricos
        numeric_configs = [
            ("processing.max_file_size_mb", 1, 1000),
            ("processing.max_workers", 1, 16),
            ("output.max_output_files", 10, 1000),
            ("history.max_recent_directories", 5, 50),
            ("history.max_recent_files", 10, 100)
        ]
        
        for config_key, min_val, max_val in numeric_configs:
            value = self.get(config_key, 0)
            if not isinstance(value, (int, float)) or value < min_val or value > max_val:
                default_value = self.DEFAULT_CONFIG
                for key in config_key.split('.'):
                    default_value = default_value[key]
                self.set(config_key, default_value)
                changes_made = True
        
        if changes_made:
            self.save_config()
        
        return changes_made

