"""
Módulo de processamento de arquivos para UltraTexto Pro
"""

import os
import time
from pathlib import Path
from typing import List, Dict, Set, Optional, Callable, Generator
from datetime import datetime
import threading
import queue

class FileInfo:
    """Classe para armazenar informações de um arquivo"""
    
    def __init__(self, path: str):
        self.path = Path(path)
        self.name = self.path.name
        self.extension = self.path.suffix.lower()
        self.size = 0
        self.modified_time = None
        self.is_directory = False
        self.is_excluded = False
        self.exclusion_reason = ""
        
        try:
            stat = self.path.stat()
            self.size = stat.st_size
            self.modified_time = datetime.fromtimestamp(stat.st_mtime)
            self.is_directory = self.path.is_dir()
        except (OSError, ValueError):
            pass
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            'path': str(self.path),
            'name': self.name,
            'extension': self.extension,
            'size': self.size,
            'modified_time': self.modified_time.isoformat() if self.modified_time else None,
            'is_directory': self.is_directory,
            'is_excluded': self.is_excluded,
            'exclusion_reason': self.exclusion_reason
        }

class ProcessingStats:
    """Classe para estatísticas de processamento"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.total_files = 0
        self.processed_files = 0
        self.excluded_files = 0
        self.total_directories = 0
        self.excluded_directories = 0
        self.total_size = 0
        self.processed_size = 0
        self.errors = []
        self.supported_extensions = set()
        self.found_extensions = set()
    
    @property
    def duration(self) -> float:
        """Duração do processamento em segundos"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0
    
    @property
    def processing_speed(self) -> float:
        """Velocidade de processamento (arquivos/segundo)"""
        if self.duration > 0:
            return self.processed_files / self.duration
        return 0
    
    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.duration,
            'total_files': self.total_files,
            'processed_files': self.processed_files,
            'excluded_files': self.excluded_files,
            'total_directories': self.total_directories,
            'excluded_directories': self.excluded_directories,
            'total_size': self.total_size,
            'processed_size': self.processed_size,
            'processing_speed': self.processing_speed,
            'errors': self.errors,
            'supported_extensions': list(self.supported_extensions),
            'found_extensions': list(self.found_extensions)
        }

class FileProcessor:
    """Processador principal de arquivos"""
    
    def __init__(self, supported_extensions: Set[str], exclusion_manager=None):
        self.supported_extensions = supported_extensions
        self.exclusion_manager = exclusion_manager
        self.stats = ProcessingStats()
        self.cancelled = False
        self.progress_callback: Optional[Callable] = None
        self.status_callback: Optional[Callable] = None
        
        # Thread safety
        self._lock = threading.Lock()
        self._progress_queue = queue.Queue()
    
    def set_progress_callback(self, callback: Callable):
        """Define callback para progresso"""
        self.progress_callback = callback
    
    def set_status_callback(self, callback: Callable):
        """Define callback para status"""
        self.status_callback = callback
    
    def cancel(self):
        """Cancela o processamento"""
        self.cancelled = True
    
    def _update_progress(self, current: int, total: int, message: str = ""):
        """Atualiza o progresso"""
        if self.progress_callback:
            try:
                self.progress_callback(current, total, message)
            except:
                pass
    
    def _update_status(self, status: str):
        """Atualiza o status"""
        if self.status_callback:
            try:
                self.status_callback(status)
            except:
                pass
    
    def scan_directory(self, root_path: str, include_subdirectories: bool = True) -> Generator[FileInfo, None, None]:
        """
        Escaneia diretório e retorna informações dos arquivos
        """
        self._update_status("Escaneando diretório...")
        
        root_path = Path(root_path)
        if not root_path.exists():
            raise ValueError(f"Diretório não encontrado: {root_path}")
        
        scanned_count = 0
        
        if include_subdirectories:
            # Usar os.walk para incluir subdiretórios
            for root, dirs, files in os.walk(root_path):
                if self.cancelled:
                    break
                
                # Verificar diretórios para exclusão
                dirs_to_remove = []
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    file_info = FileInfo(dir_path)
                    
                    # Verificar exclusão
                    if self.exclusion_manager:
                        should_exclude, reason = self.exclusion_manager.should_exclude_path(
                            dir_path, is_directory=True
                        )
                        if should_exclude:
                            file_info.is_excluded = True
                            file_info.exclusion_reason = reason
                            dirs_to_remove.append(dir_name)
                            self.stats.excluded_directories += 1
                    
                    self.stats.total_directories += 1
                    yield file_info
                    scanned_count += 1
                    
                    if scanned_count % 100 == 0:
                        self._update_progress(scanned_count, -1, f"Escaneados: {scanned_count}")
                
                # Remover diretórios excluídos da lista para não entrar neles
                for dir_name in dirs_to_remove:
                    dirs.remove(dir_name)
                
                # Processar arquivos
                for file_name in files:
                    if self.cancelled:
                        break
                    
                    file_path = os.path.join(root, file_name)
                    file_info = FileInfo(file_path)
                    
                    # Verificar exclusão
                    if self.exclusion_manager:
                        should_exclude, reason = self.exclusion_manager.should_exclude_path(
                            file_path, is_directory=False
                        )
                        if should_exclude:
                            file_info.is_excluded = True
                            file_info.exclusion_reason = reason
                            self.stats.excluded_files += 1
                    
                    self.stats.total_files += 1
                    self.stats.total_size += file_info.size
                    self.stats.found_extensions.add(file_info.extension)
                    
                    yield file_info
                    scanned_count += 1
                    
                    if scanned_count % 100 == 0:
                        self._update_progress(scanned_count, -1, f"Escaneados: {scanned_count}")
        
        else:
            # Apenas o diretório raiz
            try:
                for item in root_path.iterdir():
                    if self.cancelled:
                        break
                    
                    file_info = FileInfo(item)
                    
                    # Verificar exclusão
                    if self.exclusion_manager:
                        should_exclude, reason = self.exclusion_manager.should_exclude_path(
                            str(item), is_directory=file_info.is_directory
                        )
                        if should_exclude:
                            file_info.is_excluded = True
                            file_info.exclusion_reason = reason
                            if file_info.is_directory:
                                self.stats.excluded_directories += 1
                            else:
                                self.stats.excluded_files += 1
                    
                    if file_info.is_directory:
                        self.stats.total_directories += 1
                    else:
                        self.stats.total_files += 1
                        self.stats.total_size += file_info.size
                        self.stats.found_extensions.add(file_info.extension)
                    
                    yield file_info
                    scanned_count += 1
                    
                    if scanned_count % 100 == 0:
                        self._update_progress(scanned_count, -1, f"Escaneados: {scanned_count}")
            
            except PermissionError as e:
                self.stats.errors.append(f"Erro de permissão: {e}")
    
    def process_files_content(self, root_path: str, output_path: str, 
                            include_subdirectories: bool = True) -> str:
        """
        Processa arquivos e extrai conteúdo para arquivo de texto
        """
        self.stats = ProcessingStats()
        self.stats.start_time = datetime.now()
        self.stats.supported_extensions = self.supported_extensions.copy()
        self.cancelled = False
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as output_file:
                # Cabeçalho
                output_file.write(f"# Conteúdo dos Arquivos - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                output_file.write(f"# Diretório: {root_path}\n")
                output_file.write(f"# Extensões suportadas: {', '.join(sorted(self.supported_extensions))}\n")
                output_file.write("=" * 80 + "\n\n")
                
                # Escanear e processar arquivos
                files_to_process = []
                self._update_status("Escaneando arquivos...")
                
                for file_info in self.scan_directory(root_path, include_subdirectories):
                    if self.cancelled:
                        break
                    
                    # Apenas arquivos não excluídos e com extensões suportadas
                    if (not file_info.is_directory and 
                        not file_info.is_excluded and 
                        file_info.extension in self.supported_extensions):
                        files_to_process.append(file_info)
                
                total_files = len(files_to_process)
                self._update_status(f"Processando {total_files} arquivos...")
                
                # Processar cada arquivo
                for i, file_info in enumerate(files_to_process):
                    if self.cancelled:
                        break
                    
                    try:
                        self._update_progress(i + 1, total_files, f"Processando: {file_info.name}")
                        
                        # Cabeçalho do arquivo
                        relative_path = os.path.relpath(file_info.path, root_path)
                        output_file.write(f"## Arquivo: {relative_path}\n")
                        output_file.write(f"**Tamanho:** {self._format_file_size(file_info.size)}\n")
                        output_file.write(f"**Modificado:** {file_info.modified_time.strftime('%Y-%m-%d %H:%M:%S') if file_info.modified_time else 'N/A'}\n\n")
                        output_file.write("```" + file_info.extension.lstrip('.') + "\n")
                        
                        # Ler conteúdo do arquivo
                        try:
                            with open(file_info.path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                output_file.write(content)
                        except UnicodeDecodeError:
                            # Tentar outras codificações
                            encodings = ['latin-1', 'cp1252', 'iso-8859-1']
                            content_read = False
                            
                            for encoding in encodings:
                                try:
                                    with open(file_info.path, 'r', encoding=encoding) as f:
                                        content = f.read()
                                        output_file.write(content)
                                        content_read = True
                                        break
                                except UnicodeDecodeError:
                                    continue
                            
                            if not content_read:
                                output_file.write("[ERRO: Não foi possível ler o arquivo - codificação não suportada]")
                        
                        except Exception as e:
                            output_file.write(f"[ERRO: {str(e)}]")
                            self.stats.errors.append(f"Erro ao ler {file_info.path}: {e}")
                        
                        output_file.write("\n```\n\n")
                        output_file.write("-" * 80 + "\n\n")
                        
                        self.stats.processed_files += 1
                        self.stats.processed_size += file_info.size
                        
                    except Exception as e:
                        self.stats.errors.append(f"Erro ao processar {file_info.path}: {e}")
                
                # Rodapé com estatísticas
                output_file.write("\n" + "=" * 80 + "\n")
                output_file.write("# Estatísticas do Processamento\n\n")
                output_file.write(f"- **Arquivos processados:** {self.stats.processed_files}\n")
                output_file.write(f"- **Arquivos excluídos:** {self.stats.excluded_files}\n")
                output_file.write(f"- **Diretórios excluídos:** {self.stats.excluded_directories}\n")
                output_file.write(f"- **Tamanho total processado:** {self._format_file_size(self.stats.processed_size)}\n")
                output_file.write(f"- **Extensões encontradas:** {', '.join(sorted(self.stats.found_extensions))}\n")
                
                if self.stats.errors:
                    output_file.write(f"- **Erros:** {len(self.stats.errors)}\n")
                    for error in self.stats.errors[:10]:  # Limitar a 10 erros
                        output_file.write(f"  - {error}\n")
                    if len(self.stats.errors) > 10:
                        output_file.write(f"  - ... e mais {len(self.stats.errors) - 10} erros\n")
        
        except Exception as e:
            self.stats.errors.append(f"Erro ao criar arquivo de saída: {e}")
            raise
        
        finally:
            self.stats.end_time = datetime.now()
        
        return str(output_path)
    
    def generate_directory_structure(self, root_path: str, output_path: str,
                                   include_subdirectories: bool = True,
                                   include_files: bool = True,
                                   format_type: str = 'text') -> str:
        """
        Gera estrutura de diretórios
        """
        self.stats = ProcessingStats()
        self.stats.start_time = datetime.now()
        self.cancelled = False
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if format_type == 'text':
                return self._generate_text_structure(root_path, output_path, include_subdirectories, include_files)
            elif format_type == 'json':
                return self._generate_json_structure(root_path, output_path, include_subdirectories, include_files)
            elif format_type == 'html':
                return self._generate_html_structure(root_path, output_path, include_subdirectories, include_files)
            else:
                raise ValueError(f"Formato não suportado: {format_type}")
        
        finally:
            self.stats.end_time = datetime.now()
    
    def _generate_text_structure(self, root_path: str, output_path: Path,
                               include_subdirectories: bool, include_files: bool) -> str:
        """Gera estrutura em formato texto"""
        with open(output_path, 'w', encoding='utf-8') as output_file:
            # Cabeçalho
            output_file.write(f"# Estrutura de Diretórios - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            output_file.write(f"# Diretório: {root_path}\n")
            output_file.write("=" * 80 + "\n\n")
            
            # Gerar árvore
            self._write_directory_tree(output_file, root_path, "", include_subdirectories, include_files)
            
            # Estatísticas
            output_file.write("\n" + "=" * 80 + "\n")
            output_file.write("# Estatísticas\n\n")
            output_file.write(f"- **Total de diretórios:** {self.stats.total_directories}\n")
            output_file.write(f"- **Total de arquivos:** {self.stats.total_files}\n")
            output_file.write(f"- **Diretórios excluídos:** {self.stats.excluded_directories}\n")
            output_file.write(f"- **Arquivos excluídos:** {self.stats.excluded_files}\n")
            output_file.write(f"- **Tamanho total:** {self._format_file_size(self.stats.total_size)}\n")
            output_file.write(f"- **Extensões encontradas:** {', '.join(sorted(self.stats.found_extensions))}\n")
        
        return str(output_path)
    
    def _write_directory_tree(self, output_file, current_path: str, prefix: str,
                            include_subdirectories: bool, include_files: bool):
        """Escreve árvore de diretórios recursivamente"""
        try:
            items = list(Path(current_path).iterdir())
            items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            
            for i, item in enumerate(items):
                if self.cancelled:
                    break
                
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                next_prefix = prefix + ("    " if is_last else "│   ")
                
                file_info = FileInfo(item)
                
                # Verificar exclusão
                if self.exclusion_manager:
                    should_exclude, reason = self.exclusion_manager.should_exclude_path(
                        str(item), is_directory=file_info.is_directory
                    )
                    if should_exclude:
                        file_info.is_excluded = True
                        file_info.exclusion_reason = reason
                
                if file_info.is_directory:
                    self.stats.total_directories += 1
                    if file_info.is_excluded:
                        self.stats.excluded_directories += 1
                        icon = "📁❌"
                    else:
                        icon = "📁"
                    
                    output_file.write(f"{prefix}{current_prefix}{icon} {file_info.name}/")
                    if file_info.is_excluded:
                        output_file.write(f" [EXCLUÍDO: {file_info.exclusion_reason}]")
                    output_file.write("\n")
                    
                    # Recursão para subdiretórios (se não excluído e incluir subdiretórios)
                    if include_subdirectories and not file_info.is_excluded:
                        self._write_directory_tree(output_file, str(item), next_prefix,
                                                 include_subdirectories, include_files)
                
                elif include_files:
                    self.stats.total_files += 1
                    self.stats.total_size += file_info.size
                    self.stats.found_extensions.add(file_info.extension)
                    
                    if file_info.is_excluded:
                        self.stats.excluded_files += 1
                        icon = "📄❌"
                    elif file_info.extension in self.supported_extensions:
                        icon = "📄✅"
                    else:
                        icon = "📄"
                    
                    size_str = self._format_file_size(file_info.size)
                    output_file.write(f"{prefix}{current_prefix}{icon} {file_info.name} ({size_str})")
                    
                    if file_info.is_excluded:
                        output_file.write(f" [EXCLUÍDO: {file_info.exclusion_reason}]")
                    
                    output_file.write("\n")
        
        except PermissionError:
            output_file.write(f"{prefix}├── ❌ [ERRO: Sem permissão de acesso]\n")
            self.stats.errors.append(f"Erro de permissão: {current_path}")
        except Exception as e:
            output_file.write(f"{prefix}├── ❌ [ERRO: {str(e)}]\n")
            self.stats.errors.append(f"Erro ao acessar {current_path}: {e}")
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Formata tamanho do arquivo"""
        if size_bytes == 0:
            return "0 B"
        
        units = ["B", "KB", "MB", "GB", "TB"]
        unit_index = 0
        size = float(size_bytes)
        
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        if unit_index == 0:
            return f"{int(size)} {units[unit_index]}"
        else:
            return f"{size:.1f} {units[unit_index]}"
    
    def get_file_count_estimate(self, root_path: str, include_subdirectories: bool = True) -> int:
        """Estima o número de arquivos para barra de progresso"""
        try:
            count = 0
            if include_subdirectories:
                for root, dirs, files in os.walk(root_path):
                    count += len(files)
                    if count > 10000:  # Limitar para não demorar muito
                        break
            else:
                count = len([f for f in Path(root_path).iterdir() if f.is_file()])
            
            return count
        except:
            return 0

