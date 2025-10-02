"""
Módulo de gerenciamento avançado de exclusões para UltraTexto Pro
"""

import os
import re
import json
import fnmatch
from pathlib import Path
from typing import List, Dict, Tuple, Set, Optional
from datetime import datetime, timedelta

class ExclusionRule:
    """Classe para representar uma regra de exclusão"""
    
    def __init__(self, rule_type: str, pattern: str, description: str = "", 
                 case_sensitive: bool = False, enabled: bool = True):
        self.rule_type = rule_type  # 'file', 'folder', 'extension', 'regex', 'size', 'date'
        self.pattern = pattern
        self.description = description
        self.case_sensitive = case_sensitive
        self.enabled = enabled
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """Converte a regra para dicionário"""
        return {
            'rule_type': self.rule_type,
            'pattern': self.pattern,
            'description': self.description,
            'case_sensitive': self.case_sensitive,
            'enabled': self.enabled,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ExclusionRule':
        """Cria regra a partir de dicionário"""
        rule = cls(
            rule_type=data['rule_type'],
            pattern=data['pattern'],
            description=data.get('description', ''),
            case_sensitive=data.get('case_sensitive', False),
            enabled=data.get('enabled', True)
        )
        if 'created_at' in data:
            rule.created_at = datetime.fromisoformat(data['created_at'])
        return rule

class ExclusionProfile:
    """Classe para representar um perfil de exclusões"""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.rules: List[ExclusionRule] = []
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
    
    def add_rule(self, rule: ExclusionRule):
        """Adiciona uma regra ao perfil"""
        self.rules.append(rule)
        self.modified_at = datetime.now()
    
    def remove_rule(self, index: int):
        """Remove uma regra do perfil"""
        if 0 <= index < len(self.rules):
            del self.rules[index]
            self.modified_at = datetime.now()
    
    def get_enabled_rules(self) -> List[ExclusionRule]:
        """Retorna apenas as regras habilitadas"""
        return [rule for rule in self.rules if rule.enabled]
    
    def to_dict(self) -> Dict:
        """Converte o perfil para dicionário"""
        return {
            'name': self.name,
            'description': self.description,
            'rules': [rule.to_dict() for rule in self.rules],
            'created_at': self.created_at.isoformat(),
            'modified_at': self.modified_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ExclusionProfile':
        """Cria perfil a partir de dicionário"""
        profile = cls(data['name'], data.get('description', ''))
        profile.rules = [ExclusionRule.from_dict(rule_data) for rule_data in data.get('rules', [])]
        if 'created_at' in data:
            profile.created_at = datetime.fromisoformat(data['created_at'])
        if 'modified_at' in data:
            profile.modified_at = datetime.fromisoformat(data['modified_at'])
        return profile

class ExclusionManager:
    """Gerenciador avançado de exclusões"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        self.profiles_file = self.config_dir / "exclusion_profiles.json"
        
        self.profiles: Dict[str, ExclusionProfile] = {}
        self.current_profile: Optional[ExclusionProfile] = None
        
        # Carregar perfis salvos
        self.load_profiles()
        
        # Criar perfil padrão se não existir
        if not self.profiles:
            self.create_default_profile()
    
    def create_default_profile(self):
        """Cria perfil padrão com exclusões comuns para pastas grandes e desnecessárias"""
        default_profile = ExclusionProfile("Padrão", "Perfil padrão com exclusões comuns para pastas grandes e desnecessárias")
        
        # Adicionar regras padrão para pastas grandes
        common_exclusions = [
            # Ambientes virtuais Python
            ExclusionRule('folder', '.venv', 'Ambiente virtual Python (.venv)'),
            ExclusionRule('folder', 'venv', 'Ambiente virtual Python (venv)'),
            ExclusionRule('folder', 'env', 'Ambiente virtual Python (env)'),
            
            # Dependências Node.js
            ExclusionRule('folder', 'node_modules', 'Dependências Node.js'),
            
            # Dependências PHP/Composer
            ExclusionRule('folder', 'vendor', 'Dependências PHP/Composer'),
            ExclusionRule('folder', 'composer', 'Cache Composer PHP'),
            
            # Dependências Java
            ExclusionRule('folder', 'target', 'Arquivos de build Java/Rust'),
            ExclusionRule('folder', '.gradle', 'Cache Gradle'),
            ExclusionRule('folder', '.m2', 'Cache Maven'),
            
            # Dependências .NET
            ExclusionRule('folder', 'obj', 'Arquivos de objeto .NET'),
            ExclusionRule('folder', 'packages', 'Pacotes NuGet/.NET'),
            ExclusionRule('folder', 'bin', 'Arquivos binários'),
            
            # Cache e dependências JavaScript
            ExclusionRule('folder', '.npm', 'Cache NPM'),
            ExclusionRule('folder', '.yarn', 'Cache Yarn'),
            
            # Repositórios e controle de versão
            ExclusionRule('folder', '.git', 'Repositório Git'),
            ExclusionRule('folder', '.svn', 'Repositório SVN'),
            ExclusionRule('folder', '.hg', 'Repositório Mercurial'),
            
            # Cache Python
            ExclusionRule('folder', '__pycache__', 'Cache Python'),
            ExclusionRule('folder', '.pytest_cache', 'Cache Pytest'),
            
            # Arquivos de build e distribuição
            ExclusionRule('folder', 'dist', 'Arquivos de distribuição'),
            ExclusionRule('folder', 'build', 'Arquivos de build'),
            ExclusionRule('folder', 'out', 'Arquivos de saída'),
            ExclusionRule('folder', 'release', 'Arquivos de release'),
            
            # Configurações de IDEs
            ExclusionRule('folder', '.vscode', 'Configurações VS Code'),
            ExclusionRule('folder', '.idea', 'Configurações IntelliJ/PhpStorm'),
            ExclusionRule('folder', '.vs', 'Configurações Visual Studio'),
            ExclusionRule('folder', '.eclipse', 'Configurações Eclipse'),
            
            # Logs e arquivos temporários
            ExclusionRule('folder', 'logs', 'Arquivos de log'),
            ExclusionRule('folder', 'temp', 'Arquivos temporários'),
            ExclusionRule('folder', 'tmp', 'Arquivos temporários'),
            ExclusionRule('folder', 'coverage', 'Relatórios de cobertura de testes'),
            
            # Extensões de arquivos comuns
            ExclusionRule('extension', '.log', 'Arquivos de log'),
            ExclusionRule('extension', '.tmp', 'Arquivos temporários'),
            ExclusionRule('extension', '.cache', 'Arquivos de cache'),
            ExclusionRule('extension', '.env', 'Arquivos de variáveis de ambiente'),
            
            # Regex para arquivos específicos
            ExclusionRule('regex', r'.*\.min\.(js|css)$', 'Arquivos minificados'),
            ExclusionRule('regex', r'.*\.(exe|dll|so|dylib)$', 'Arquivos binários'),
            ExclusionRule('regex', r'.*\.(zip|rar|7z|tar|gz)$', 'Arquivos compactados'),
            ExclusionRule('regex', r'.*\.(mp4|avi|mov|mkv|wmv)$', 'Arquivos de vídeo'),
            ExclusionRule('regex', r'.*\.(mp3|wav|flac|aac)$', 'Arquivos de áudio'),
            ExclusionRule('regex', r'.*\.(jpg|jpeg|png|gif|bmp|tiff|svg)$', 'Arquivos de imagem'),
        ]
        
        for rule in common_exclusions:
            default_profile.add_rule(rule)
        
        self.profiles["Padrão"] = default_profile
        self.current_profile = default_profile
        self.save_profiles()
    
    def create_profile(self, name: str, description: str = "") -> ExclusionProfile:
        """Cria um novo perfil"""
        if name in self.profiles:
            raise ValueError(f"Perfil '{name}' já existe")
        
        profile = ExclusionProfile(name, description)
        self.profiles[name] = profile
        self.save_profiles()
        return profile
    
    def delete_profile(self, name: str):
        """Exclui um perfil"""
        if name not in self.profiles:
            raise ValueError(f"Perfil '{name}' não encontrado")
        
        if name == "Padrão":
            raise ValueError("Não é possível excluir o perfil padrão")
        
        del self.profiles[name]
        
        # Se era o perfil atual, voltar para o padrão
        if self.current_profile and self.current_profile.name == name:
            self.current_profile = self.profiles.get("Padrão")
        
        self.save_profiles()
    
    def set_current_profile(self, name: str):
        """Define o perfil atual"""
        if name not in self.profiles:
            raise ValueError(f"Perfil '{name}' não encontrado")
        
        self.current_profile = self.profiles[name]
    
    def add_rule_to_current_profile(self, rule: ExclusionRule):
        """Adiciona regra ao perfil atual"""
        if self.current_profile:
            self.current_profile.add_rule(rule)
            self.save_profiles()
    
    def remove_rule_from_current_profile(self, index: int):
        """Remove regra do perfil atual"""
        if self.current_profile:
            self.current_profile.remove_rule(index)
            self.save_profiles()
    
    def should_exclude_path(self, file_path: str, is_directory: bool = False) -> Tuple[bool, str]:
        """
        Verifica se um caminho deve ser excluído
        Retorna (should_exclude, reason)
        """
        if not self.current_profile:
            return False, ""
        
        path_obj = Path(file_path)
        
        for rule in self.current_profile.get_enabled_rules():
            if self._matches_rule(path_obj, rule, is_directory):
                return True, f"Regra: {rule.description or rule.pattern}"
        
        return False, ""
    
    def _matches_rule(self, path: Path, rule: ExclusionRule, is_directory: bool) -> bool:
        """Verifica se um caminho corresponde a uma regra"""
        pattern = rule.pattern
        if not rule.case_sensitive:
            pattern = pattern.lower()
            path_str = str(path).lower()
            name = path.name.lower()
        else:
            path_str = str(path)
            name = path.name
        
        if rule.rule_type == 'file':
            return not is_directory and (path_str == pattern or name == pattern)
        
        elif rule.rule_type == 'folder':
            return is_directory and (path_str == pattern or name == pattern or pattern in path_str)
        
        elif rule.rule_type == 'extension':
            if is_directory:
                return False
            ext = path.suffix
            if not rule.case_sensitive:
                ext = ext.lower()
            return ext == pattern or ext == f".{pattern.lstrip('.')}"
        
        elif rule.rule_type == 'regex':
            try:
                flags = 0 if rule.case_sensitive else re.IGNORECASE
                return bool(re.match(pattern, path_str, flags))
            except re.error:
                return False
        
        elif rule.rule_type == 'wildcard':
            return fnmatch.fnmatch(path_str, pattern)
        
        elif rule.rule_type == 'size':
            if is_directory:
                return False
            try:
                file_size = path.stat().st_size
                return self._matches_size_pattern(file_size, pattern)
            except (OSError, ValueError):
                return False
        
        elif rule.rule_type == 'date':
            try:
                file_mtime = datetime.fromtimestamp(path.stat().st_mtime)
                return self._matches_date_pattern(file_mtime, pattern)
            except (OSError, ValueError):
                return False
        
        return False
    
    def _matches_size_pattern(self, file_size: int, pattern: str) -> bool:
        """Verifica se o tamanho do arquivo corresponde ao padrão"""
        # Padrões: >1MB, <500KB, =0B, etc.
        pattern = pattern.strip().upper()
        
        # Extrair operador e valor
        if pattern.startswith('>='):
            operator = '>='
            size_str = pattern[2:]
        elif pattern.startswith('<='):
            operator = '<='
            size_str = pattern[2:]
        elif pattern.startswith('>'):
            operator = '>'
            size_str = pattern[1:]
        elif pattern.startswith('<'):
            operator = '<'
            size_str = pattern[1:]
        elif pattern.startswith('='):
            operator = '='
            size_str = pattern[1:]
        else:
            operator = '='
            size_str = pattern
        
        # Converter tamanho para bytes
        try:
            size_bytes = self._parse_size_string(size_str)
        except ValueError:
            return False
        
        # Aplicar operador
        if operator == '>':
            return file_size > size_bytes
        elif operator == '>=':
            return file_size >= size_bytes
        elif operator == '<':
            return file_size < size_bytes
        elif operator == '<=':
            return file_size <= size_bytes
        elif operator == '=':
            return file_size == size_bytes
        
        return False
    
    def _parse_size_string(self, size_str: str) -> int:
        """Converte string de tamanho para bytes"""
        size_str = size_str.strip().upper()
        
        # Unidades
        units = {
            'B': 1,
            'KB': 1024,
            'MB': 1024 ** 2,
            'GB': 1024 ** 3,
            'TB': 1024 ** 4
        }
        
        # Extrair número e unidade
        for unit, multiplier in units.items():
            if size_str.endswith(unit):
                number_str = size_str[:-len(unit)].strip()
                try:
                    number = float(number_str)
                    return int(number * multiplier)
                except ValueError:
                    continue
        
        # Se não tem unidade, assumir bytes
        try:
            return int(float(size_str))
        except ValueError:
            raise ValueError(f"Formato de tamanho inválido: {size_str}")
    
    def _matches_date_pattern(self, file_date: datetime, pattern: str) -> bool:
        """Verifica se a data do arquivo corresponde ao padrão"""
        # Padrões: >2023-01-01, <30d, =today, etc.
        pattern = pattern.strip().lower()
        now = datetime.now()
        
        if pattern.startswith('>'):
            date_str = pattern[1:]
            target_date = self._parse_date_string(date_str, now)
            return file_date > target_date
        elif pattern.startswith('<'):
            date_str = pattern[1:]
            target_date = self._parse_date_string(date_str, now)
            return file_date < target_date
        elif pattern.startswith('='):
            date_str = pattern[1:]
            target_date = self._parse_date_string(date_str, now)
            return file_date.date() == target_date.date()
        
        return False
    
    def _parse_date_string(self, date_str: str, reference_date: datetime) -> datetime:
        """Converte string de data para datetime"""
        date_str = date_str.strip().lower()
        
        # Palavras-chave especiais
        if date_str == 'today':
            return reference_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_str == 'yesterday':
            return (reference_date - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Padrões relativos (30d, 1w, 6m, 1y)
        if date_str.endswith('d'):
            days = int(date_str[:-1])
            return reference_date - timedelta(days=days)
        elif date_str.endswith('w'):
            weeks = int(date_str[:-1])
            return reference_date - timedelta(weeks=weeks)
        elif date_str.endswith('m'):
            months = int(date_str[:-1])
            return reference_date - timedelta(days=months * 30)  # Aproximação
        elif date_str.endswith('y'):
            years = int(date_str[:-1])
            return reference_date - timedelta(days=years * 365)  # Aproximação
        
        # Formato de data absoluta (YYYY-MM-DD)
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            pass
        
        # Formato de data com hora (YYYY-MM-DD HH:MM)
        try:
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        except ValueError:
            pass
        
        raise ValueError(f"Formato de data inválido: {date_str}")
    
    def get_exclusion_preview(self, root_path: str, max_items: int = 1000) -> Dict[str, List[str]]:
        """
        Gera preview dos arquivos que serão excluídos
        Retorna dicionário com 'excluded' e 'included'
        """
        excluded = []
        included = []
        count = 0
        
        for root, dirs, files in os.walk(root_path):
            if count >= max_items:
                break
            
            # Verificar diretórios
            for dir_name in dirs[:]:
                if count >= max_items:
                    break
                
                dir_path = os.path.join(root, dir_name)
                should_exclude, reason = self.should_exclude_path(dir_path, is_directory=True)
                
                if should_exclude:
                    excluded.append(f"📁 {dir_path} ({reason})")
                    dirs.remove(dir_name)  # Não entrar no diretório
                else:
                    included.append(f"📁 {dir_path}")
                
                count += 1
            
            # Verificar arquivos
            for file_name in files:
                if count >= max_items:
                    break
                
                file_path = os.path.join(root, file_name)
                should_exclude, reason = self.should_exclude_path(file_path, is_directory=False)
                
                if should_exclude:
                    excluded.append(f"📄 {file_path} ({reason})")
                else:
                    included.append(f"📄 {file_path}")
                
                count += 1
        
        return {
            'excluded': excluded,
            'included': included,
            'total_checked': count,
            'truncated': count >= max_items
        }
    
    def save_profiles(self):
        """Salva os perfis no arquivo de configuração"""
        try:
            data = {
                'profiles': {name: profile.to_dict() for name, profile in self.profiles.items()},
                'current_profile': self.current_profile.name if self.current_profile else None
            }
            
            with open(self.profiles_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            print(f"Erro ao salvar perfis: {e}")
    
    def load_profiles(self):
        """Carrega os perfis do arquivo de configuração"""
        try:
            if self.profiles_file.exists():
                with open(self.profiles_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Carregar perfis
                for name, profile_data in data.get('profiles', {}).items():
                    self.profiles[name] = ExclusionProfile.from_dict(profile_data)
                
                # Definir perfil atual
                current_name = data.get('current_profile')
                if current_name and current_name in self.profiles:
                    self.current_profile = self.profiles[current_name]
        
        except Exception as e:
            print(f"Erro ao carregar perfis: {e}")
    
    def export_profile(self, profile_name: str, file_path: str):
        """Exporta um perfil para arquivo"""
        if profile_name not in self.profiles:
            raise ValueError(f"Perfil '{profile_name}' não encontrado")
        
        profile_data = self.profiles[profile_name].to_dict()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, indent=2, ensure_ascii=False)
    
    def import_profile(self, file_path: str, new_name: str = None):
        """Importa um perfil de arquivo"""
        with open(file_path, 'r', encoding='utf-8') as f:
            profile_data = json.load(f)
        
        profile = ExclusionProfile.from_dict(profile_data)
        
        if new_name:
            profile.name = new_name
        
        # Evitar conflitos de nome
        original_name = profile.name
        counter = 1
        while profile.name in self.profiles:
            profile.name = f"{original_name} ({counter})"
            counter += 1
        
        self.profiles[profile.name] = profile
        self.save_profiles()
        
        return profile.name
    
    def get_statistics(self) -> Dict:
        """Retorna estatísticas dos perfis e regras"""
        total_profiles = len(self.profiles)
        total_rules = sum(len(profile.rules) for profile in self.profiles.values())
        enabled_rules = sum(len(profile.get_enabled_rules()) for profile in self.profiles.values())
        
        rule_types = {}
        for profile in self.profiles.values():
            for rule in profile.rules:
                rule_types[rule.rule_type] = rule_types.get(rule.rule_type, 0) + 1
        
        return {
            'total_profiles': total_profiles,
            'total_rules': total_rules,
            'enabled_rules': enabled_rules,
            'rule_types': rule_types,
            'current_profile': self.current_profile.name if self.current_profile else None
        }

    def apply_auto_exclusions(self, config_manager=None):
        """Aplica exclusões automáticas baseadas na configuração"""
        if config_manager and config_manager.get("exclusions.auto_exclude_common", True):
            # Verificar se o perfil padrão existe e tem as exclusões necessárias
            if "Padrão" not in self.profiles:
                self.create_default_profile()
            else:
                # Verificar se precisa atualizar o perfil padrão
                default_profile = self.profiles["Padrão"]
                has_venv_exclusions = any(
                    rule.pattern in ['.venv', 'venv', 'env'] and rule.rule_type == 'folder'
                    for rule in default_profile.rules
                )
                
                if not has_venv_exclusions:
                    # Adicionar exclusões que podem estar faltando
                    missing_exclusions = [
                        ExclusionRule('folder', '.venv', 'Ambiente virtual Python (.venv)'),
                        ExclusionRule('folder', 'venv', 'Ambiente virtual Python (venv)'),
                        ExclusionRule('folder', 'env', 'Ambiente virtual Python (env)'),
                    ]
                    
                    for rule in missing_exclusions:
                        # Verificar se já não existe
                        if not any(existing.pattern == rule.pattern and existing.rule_type == rule.rule_type 
                                  for existing in default_profile.rules):
                            default_profile.add_rule(rule)
                    
                    self.save_profiles()
            
            # Garantir que o perfil padrão está ativo
            if not self.current_profile or self.current_profile.name != "Padrão":
                self.set_current_profile("Padrão")
    
    def get_exclusion_summary(self) -> Dict:
        """Retorna um resumo das exclusões ativas"""
        if not self.current_profile:
            return {"error": "Nenhum perfil ativo"}
        
        enabled_rules = self.current_profile.get_enabled_rules()
        
        summary = {
            "profile_name": self.current_profile.name,
            "total_rules": len(self.current_profile.rules),
            "enabled_rules": len(enabled_rules),
            "rule_types": {},
            "common_exclusions": []
        }
        
        # Contar por tipo de regra
        for rule in enabled_rules:
            rule_type = rule.rule_type
            if rule_type not in summary["rule_types"]:
                summary["rule_types"][rule_type] = 0
            summary["rule_types"][rule_type] += 1
            
            # Adicionar exclusões comuns à lista
            if rule.rule_type == 'folder':
                summary["common_exclusions"].append(rule.pattern)
        
        return summary

