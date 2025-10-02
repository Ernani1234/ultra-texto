"""
Módulo de escaneamento avançado de diretórios para UltraTexto Pro
"""

import os
import time
from pathlib import Path
from typing import Dict, List, Set, Optional, Generator, Tuple
from datetime import datetime
import threading
from collections import defaultdict

class DirectoryNode:
    """Representa um nó na árvore de diretórios"""
    
    def __init__(self, path: str, name: str = None):
        self.path = Path(path)
        self.name = name or self.path.name
        self.is_directory = self.path.is_dir()
        self.size = 0
        self.file_count = 0
        self.directory_count = 0
        self.modified_time = None
        self.children: List['DirectoryNode'] = []
        self.parent: Optional['DirectoryNode'] = None
        self.is_excluded = False
        self.exclusion_reason = ""
        self.extension = self.path.suffix.lower() if not self.is_directory else ""
        self.is_supported = False
        self.depth = 0
        
        # Carregar informações do arquivo/diretório
        self._load_info()
    
    def _load_info(self):
        """Carrega informações do arquivo/diretório"""
        try:
            stat = self.path.stat()
            if not self.is_directory:
                self.size = stat.st_size
            self.modified_time = datetime.fromtimestamp(stat.st_mtime)
        except (OSError, ValueError):
            pass
    
    def add_child(self, child: 'DirectoryNode'):
        """Adiciona um filho ao nó"""
        child.parent = self
        child.depth = self.depth + 1
        self.children.append(child)
        
        # Atualizar contadores
        if child.is_directory:
            self.directory_count += 1
        else:
            self.file_count += 1
            self.size += child.size
    
    def get_total_size(self) -> int:
        """Retorna o tamanho total incluindo filhos"""
        total = self.size
        for child in self.children:
            total += child.get_total_size()
        return total
    
    def get_total_file_count(self) -> int:
        """Retorna o número total de arquivos incluindo filhos"""
        total = self.file_count
        for child in self.children:
            total += child.get_total_file_count()
        return total
    
    def get_total_directory_count(self) -> int:
        """Retorna o número total de diretórios incluindo filhos"""
        total = self.directory_count
        for child in self.children:
            total += child.get_total_directory_count()
        return total
    
    def get_extension_distribution(self) -> Dict[str, int]:
        """Retorna distribuição de extensões"""
        distribution = defaultdict(int)
        
        if not self.is_directory and self.extension:
            distribution[self.extension] += 1
        
        for child in self.children:
            child_dist = child.get_extension_distribution()
            for ext, count in child_dist.items():
                distribution[ext] += count
        
        return dict(distribution)
    
    def find_nodes(self, predicate) -> List['DirectoryNode']:
        """Encontra nós que satisfazem o predicado"""
        results = []
        
        if predicate(self):
            results.append(self)
        
        for child in self.children:
            results.extend(child.find_nodes(predicate))
        
        return results
    
    def to_dict(self, include_children: bool = True) -> Dict:
        """Converte o nó para dicionário"""
        data = {
            'path': str(self.path),
            'name': self.name,
            'is_directory': self.is_directory,
            'size': self.size,
            'file_count': self.file_count,
            'directory_count': self.directory_count,
            'modified_time': self.modified_time.isoformat() if self.modified_time else None,
            'is_excluded': self.is_excluded,
            'exclusion_reason': self.exclusion_reason,
            'extension': self.extension,
            'is_supported': self.is_supported,
            'depth': self.depth,
            'total_size': self.get_total_size(),
            'total_file_count': self.get_total_file_count(),
            'total_directory_count': self.get_total_directory_count()
        }
        
        if include_children:
            data['children'] = [child.to_dict() for child in self.children]
        
        return data

class DirectoryScanner:
    """Scanner avançado de diretórios"""
    
    def __init__(self, supported_extensions: Set[str], exclusion_manager=None):
        self.supported_extensions = supported_extensions
        self.exclusion_manager = exclusion_manager
        self.cancelled = False
        self.progress_callback = None
        self.status_callback = None
        
        # Estatísticas
        self.total_items_scanned = 0
        self.total_directories = 0
        self.total_files = 0
        self.total_size = 0
        self.excluded_directories = 0
        self.excluded_files = 0
        self.errors = []
        self.extension_distribution = defaultdict(int)
        
        # Thread safety
        self._lock = threading.Lock()
    
    def set_progress_callback(self, callback):
        """Define callback para progresso"""
        self.progress_callback = callback
    
    def set_status_callback(self, callback):
        """Define callback para status"""
        self.status_callback = callback
    
    def cancel(self):
        """Cancela o escaneamento"""
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
    
    def scan_directory(self, root_path: str, include_subdirectories: bool = True,
                      max_depth: int = -1) -> DirectoryNode:
        """
        Escaneia diretório e retorna árvore de nós
        """
        self._reset_stats()
        self._update_status("Iniciando escaneamento...")
        
        root_path = Path(root_path)
        if not root_path.exists():
            raise ValueError(f"Diretório não encontrado: {root_path}")
        
        if not root_path.is_dir():
            raise ValueError(f"Caminho não é um diretório: {root_path}")
        
        # Criar nó raiz
        root_node = DirectoryNode(str(root_path))
        
        # Escanear recursivamente
        self._scan_node(root_node, include_subdirectories, max_depth)
        
        return root_node
    
    def _reset_stats(self):
        """Reseta as estatísticas"""
        self.total_items_scanned = 0
        self.total_directories = 0
        self.total_files = 0
        self.total_size = 0
        self.excluded_directories = 0
        self.excluded_files = 0
        self.errors = []
        self.extension_distribution = defaultdict(int)
    
    def _scan_node(self, node: DirectoryNode, include_subdirectories: bool, max_depth: int):
        """Escaneia um nó recursivamente"""
        if self.cancelled:
            return
        
        if max_depth >= 0 and node.depth >= max_depth:
            return
        
        try:
            items = list(node.path.iterdir())
            items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            
            for item_path in items:
                if self.cancelled:
                    break
                
                # Criar nó filho
                child_node = DirectoryNode(str(item_path))
                child_node.depth = node.depth + 1
                
                # Verificar se é extensão suportada
                if not child_node.is_directory:
                    child_node.is_supported = child_node.extension in self.supported_extensions
                
                # Verificar exclusão
                if self.exclusion_manager:
                    should_exclude, reason = self.exclusion_manager.should_exclude_path(
                        str(item_path), is_directory=child_node.is_directory
                    )
                    if should_exclude:
                        child_node.is_excluded = True
                        child_node.exclusion_reason = reason
                
                # Adicionar ao nó pai
                node.add_child(child_node)
                
                # Atualizar estatísticas
                self._update_stats(child_node)
                
                # Atualizar progresso
                self.total_items_scanned += 1
                if self.total_items_scanned % 100 == 0:
                    self._update_progress(
                        self.total_items_scanned, -1,
                        f"Escaneados: {self.total_items_scanned} itens"
                    )
                
                # Recursão para diretórios (se não excluído e incluir subdiretórios)
                if (child_node.is_directory and 
                    include_subdirectories and 
                    not child_node.is_excluded):
                    self._scan_node(child_node, include_subdirectories, max_depth)
        
        except PermissionError as e:
            error_msg = f"Erro de permissão: {node.path} - {e}"
            self.errors.append(error_msg)
            self._update_status(f"Erro de permissão: {node.path.name}")
        
        except Exception as e:
            error_msg = f"Erro ao escanear {node.path}: {e}"
            self.errors.append(error_msg)
            self._update_status(f"Erro: {node.path.name}")
    
    def _update_stats(self, node: DirectoryNode):
        """Atualiza estatísticas com base no nó"""
        with self._lock:
            if node.is_directory:
                self.total_directories += 1
                if node.is_excluded:
                    self.excluded_directories += 1
            else:
                self.total_files += 1
                self.total_size += node.size
                if node.extension:
                    self.extension_distribution[node.extension] += 1
                if node.is_excluded:
                    self.excluded_files += 1
    
    def generate_tree_text(self, root_node: DirectoryNode, 
                          show_excluded: bool = True,
                          show_sizes: bool = True,
                          max_items: int = 1000) -> str:
        """Gera representação textual da árvore"""
        lines = []
        items_count = 0
        
        def _add_node_text(node: DirectoryNode, prefix: str = "", is_last: bool = True):
            nonlocal items_count
            
            if items_count >= max_items:
                return
            
            # Pular itens excluídos se não deve mostrar
            if node.is_excluded and not show_excluded:
                return
            
            # Determinar ícone e formatação
            if node.is_directory:
                icon = "📁" if not node.is_excluded else "📁❌"
                name = f"{node.name}/"
            else:
                if node.is_excluded:
                    icon = "📄❌"
                elif node.is_supported:
                    icon = "📄✅"
                else:
                    icon = "📄"
                name = node.name
            
            # Adicionar informação de tamanho
            size_info = ""
            if show_sizes:
                if node.is_directory:
                    total_size = node.get_total_size()
                    if total_size > 0:
                        size_info = f" ({self._format_file_size(total_size)})"
                else:
                    if node.size > 0:
                        size_info = f" ({self._format_file_size(node.size)})"
            
            # Determinar prefixo da linha
            current_prefix = "└── " if is_last else "├── "
            next_prefix = prefix + ("    " if is_last else "│   ")
            
            # Adicionar linha
            line = f"{prefix}{current_prefix}{icon} {name}{size_info}"
            if node.is_excluded:
                line += f" [EXCLUÍDO: {node.exclusion_reason}]"
            
            lines.append(line)
            items_count += 1
            
            # Adicionar filhos
            if node.children and items_count < max_items:
                for i, child in enumerate(node.children):
                    if items_count >= max_items:
                        break
                    is_child_last = i == len(node.children) - 1
                    _add_node_text(child, next_prefix, is_child_last)
        
        # Adicionar nó raiz
        _add_node_text(root_node)
        
        # Adicionar indicador se truncado
        if items_count >= max_items:
            lines.append("... (lista truncada)")
        
        return "\n".join(lines)
    
    def generate_tree_items_for_export(self, root_node: DirectoryNode,
                                     show_excluded: bool = True) -> List[Dict]:
        """Gera lista de itens da árvore para exportação"""
        items = []
        
        def _add_node_items(node: DirectoryNode, prefix: str = "", is_last: bool = True):
            # Pular itens excluídos se não deve mostrar
            if node.is_excluded and not show_excluded:
                return
            
            # Determinar prefixo da linha
            current_prefix = "└── " if is_last else "├── "
            next_prefix = prefix + ("    " if is_last else "│   ")
            
            # Adicionar item
            item = {
                'name': node.name,
                'path': str(node.path),
                'is_directory': node.is_directory,
                'is_excluded': node.is_excluded,
                'exclusion_reason': node.exclusion_reason,
                'is_supported': node.is_supported,
                'size': node.size,
                'extension': node.extension,
                'depth': node.depth,
                'prefix': prefix + current_prefix
            }
            items.append(item)
            
            # Adicionar filhos
            if node.children:
                for i, child in enumerate(node.children):
                    is_child_last = i == len(node.children) - 1
                    _add_node_items(child, next_prefix, is_child_last)
        
        _add_node_items(root_node)
        return items
    
    def get_statistics(self) -> Dict:
        """Retorna estatísticas do escaneamento"""
        return {
            'total_items_scanned': self.total_items_scanned,
            'total_directories': self.total_directories,
            'total_files': self.total_files,
            'total_size': self.total_size,
            'excluded_directories': self.excluded_directories,
            'excluded_files': self.excluded_files,
            'errors_count': len(self.errors),
            'errors': self.errors,
            'extension_distribution': dict(self.extension_distribution),
            'supported_extensions': list(self.supported_extensions)
        }
    
    def search_nodes(self, root_node: DirectoryNode, query: str,
                    search_in_content: bool = False) -> List[DirectoryNode]:
        """Busca nós que correspondem à consulta"""
        query = query.lower()
        results = []
        
        def _search_predicate(node: DirectoryNode) -> bool:
            # Buscar no nome
            if query in node.name.lower():
                return True
            
            # Buscar no caminho
            if query in str(node.path).lower():
                return True
            
            # Buscar na extensão
            if query in node.extension.lower():
                return True
            
            # Buscar no conteúdo (apenas para arquivos pequenos de texto)
            if (search_in_content and 
                not node.is_directory and 
                node.size < 1024 * 1024 and  # Máximo 1MB
                node.extension in {'.txt', '.md', '.py', '.js', '.html', '.css', '.json'}):
                try:
                    with open(node.path, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        if query in content:
                            return True
                except:
                    pass
            
            return False
        
        return root_node.find_nodes(_search_predicate)
    
    def get_largest_files(self, root_node: DirectoryNode, count: int = 10) -> List[DirectoryNode]:
        """Retorna os maiores arquivos"""
        files = root_node.find_nodes(lambda n: not n.is_directory and not n.is_excluded)
        files.sort(key=lambda n: n.size, reverse=True)
        return files[:count]
    
    def get_largest_directories(self, root_node: DirectoryNode, count: int = 10) -> List[DirectoryNode]:
        """Retorna os maiores diretórios"""
        directories = root_node.find_nodes(lambda n: n.is_directory and not n.is_excluded)
        directories.sort(key=lambda n: n.get_total_size(), reverse=True)
        return directories[:count]
    
    def get_files_by_extension(self, root_node: DirectoryNode, extension: str) -> List[DirectoryNode]:
        """Retorna arquivos de uma extensão específica"""
        extension = extension.lower()
        if not extension.startswith('.'):
            extension = '.' + extension
        
        return root_node.find_nodes(
            lambda n: not n.is_directory and n.extension == extension and not n.is_excluded
        )
    
    def get_empty_directories(self, root_node: DirectoryNode) -> List[DirectoryNode]:
        """Retorna diretórios vazios"""
        return root_node.find_nodes(
            lambda n: n.is_directory and len(n.children) == 0 and not n.is_excluded
        )
    
    def get_duplicate_names(self, root_node: DirectoryNode) -> Dict[str, List[DirectoryNode]]:
        """Retorna arquivos/diretórios com nomes duplicados"""
        name_map = defaultdict(list)
        
        def _collect_names(node: DirectoryNode):
            if not node.is_excluded:
                name_map[node.name.lower()].append(node)
            for child in node.children:
                _collect_names(child)
        
        _collect_names(root_node)
        
        # Retornar apenas nomes com duplicatas
        return {name: nodes for name, nodes in name_map.items() if len(nodes) > 1}
    
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

    def clone_directory_with_exclusions(self, source_path: str, dest_path: str, include_subdirectories: bool = True, overwrite: bool = False) -> int:
        """
        Clona uma pasta inteira para outro diretório, respeitando as exclusões do ExclusionManager.
        Retorna o número de arquivos/diretórios copiados.
        """
        source_path = Path(source_path)
        dest_path = Path(dest_path)
        if not source_path.exists() or not source_path.is_dir():
            raise ValueError(f"Diretório de origem inválido: {source_path}")
        
        total_copied = 0
        for root, dirs, files in os.walk(source_path):
            rel_root = Path(root).relative_to(source_path)
            dest_root = dest_path / rel_root
            # Verificar exclusão do diretório atual
            if self.exclusion_manager:
                should_exclude, _ = self.exclusion_manager.should_exclude_path(str(root), is_directory=True)
                if should_exclude and rel_root != Path('.'):
                    # Não copia este diretório nem seus filhos
                    dirs.clear()
                    continue
            # Criar diretório de destino
            dest_root.mkdir(parents=True, exist_ok=True)
            # Copiar arquivos
            for file_name in files:
                src_file = Path(root) / file_name
                # Verificar exclusão do arquivo
                if self.exclusion_manager:
                    should_exclude, _ = self.exclusion_manager.should_exclude_path(str(src_file), is_directory=False)
                    if should_exclude:
                        continue
                dest_file = dest_root / file_name
                if dest_file.exists() and not overwrite:
                    continue
                try:
                    from shutil import copy2
                    copy2(src_file, dest_file)
                    total_copied += 1
                except Exception as e:
                    self.errors.append(f"Erro ao copiar {src_file} para {dest_file}: {e}")
            # Atualizar progresso (opcional)
        return total_copied

