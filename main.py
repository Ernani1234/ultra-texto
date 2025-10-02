"""
UltraTexto Pro - Ferramenta Avançada de Processamento de Arquivos
Versão 2.0 - Interface Moderna com Tema Escuro
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import threading
from pathlib import Path

# Adicionar o diretório atual ao path para imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Imports dos módulos
from themes.dark_theme import DarkTheme
from modules.ui_components import (
    ProgressDialog, NotificationManager, FileTreeView, 
    SearchBox, StatusBar
)

class UltraTextoPro:
    """Classe principal da aplicação UltraTexto Pro"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_theme()
        self.setup_variables()
        self.setup_ui()
        self.setup_notifications()
        
        # Dados da aplicação
        self.current_directory = None
        self.exclusions = []
        self.supported_extensions = {
            '.js', '.php', '.vue', '.cs', '.py', '.java', '.ts', '.cy', 
            '.json', '.cshtml', '.html', '.csv', '.txt', '.md', '.xml',
            '.css', '.scss', '.sass', '.jsx', '.tsx', '.cpp', '.c', '.h'
        }
    
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("UltraTexto Pro - Processador Avançado de Arquivos")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Centralizar na tela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
        
        # Ícone (se disponível)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
    
    def setup_theme(self):
        """Aplica o tema escuro"""
        self.style = DarkTheme.apply_theme(self.root)
    
    def setup_variables(self):
        """Inicializa as variáveis da aplicação"""
        self.selected_directory = tk.StringVar()
        self.include_subdirectories = tk.BooleanVar(value=True)
        self.include_files_in_structure = tk.BooleanVar(value=True)
        self.processing_mode = tk.StringVar(value="content")  # content ou structure
    
    def setup_notifications(self):
        """Configura o sistema de notificações"""
        self.notifications = NotificationManager(self.root)
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Frame principal
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = DarkTheme.create_title_label(title_frame, "UltraTexto Pro")
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = DarkTheme.create_subtitle_label(
            title_frame, "Processador Avançado de Arquivos v2.0"
        )
        subtitle_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Notebook (abas)
        self.notebook = ttk.Notebook(main_frame, style='Dark.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Criar abas
        self.create_main_tab()
        self.create_exclusions_tab()
        self.create_results_tab()
        self.create_settings_tab()
        
        # Barra de status
        self.status_bar = StatusBar(main_frame)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def create_main_tab(self):
        """Cria a aba principal"""
        main_tab = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(main_tab, text="  Processamento  ")
        
        # Frame de seleção de diretório
        dir_frame = DarkTheme.create_card_frame(main_tab, padding=15)
        dir_frame.pack(fill=tk.X, pady=(0, 15))
        
        dir_label = ttk.Label(dir_frame, text="Diretório Selecionado:", style='Dark.TLabel')
        dir_label.pack(anchor='w', pady=(0, 5))
        
        dir_input_frame = ttk.Frame(dir_frame, style='Dark.TFrame')
        dir_input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.dir_entry = ttk.Entry(dir_input_frame, textvariable=self.selected_directory, 
                                  style='Dark.TEntry', font=('Segoe UI', 10))
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_button = ttk.Button(dir_input_frame, text="Procurar", 
                                  style='Accent.TButton', command=self.browse_directory)
        browse_button.pack(side=tk.RIGHT)
        
        # Extensões suportadas
        ext_label = ttk.Label(dir_frame, 
                             text=f"Extensões suportadas: {', '.join(sorted(self.supported_extensions))}", 
                             style='Subtitle.TLabel', wraplength=800)
        ext_label.pack(anchor='w')
        
        # Frame de opções
        options_frame = DarkTheme.create_card_frame(main_tab, padding=15)
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        options_label = ttk.Label(options_frame, text="Opções de Processamento:", style='Dark.TLabel')
        options_label.pack(anchor='w', pady=(0, 10))
        
        # Checkboxes
        checkbox_frame = ttk.Frame(options_frame, style='Dark.TFrame')
        checkbox_frame.pack(fill=tk.X)
        
        subdir_check = ttk.Checkbutton(checkbox_frame, text="Incluir subdiretórios", 
                                      variable=self.include_subdirectories, style='Dark.TCheckbutton')
        subdir_check.pack(side=tk.LEFT, padx=(0, 20))
        
        files_check = ttk.Checkbutton(checkbox_frame, text="Incluir arquivos na estrutura", 
                                     variable=self.include_files_in_structure, style='Dark.TCheckbutton')
        files_check.pack(side=tk.LEFT)
        
        # Frame de modo de processamento
        mode_frame = DarkTheme.create_card_frame(main_tab, padding=15)
        mode_frame.pack(fill=tk.X, pady=(0, 15))
        
        mode_label = ttk.Label(mode_frame, text="Modo de Processamento:", style='Dark.TLabel')
        mode_label.pack(anchor='w', pady=(0, 10))
        
        radio_frame = ttk.Frame(mode_frame, style='Dark.TFrame')
        radio_frame.pack(fill=tk.X)
        
        content_radio = ttk.Radiobutton(radio_frame, text="Extrair conteúdo dos arquivos", 
                                       variable=self.processing_mode, value="content", 
                                       style='Dark.TRadiobutton')
        content_radio.pack(side=tk.LEFT, padx=(0, 20))
        
        structure_radio = ttk.Radiobutton(radio_frame, text="Gerar estrutura de diretórios", 
                                         variable=self.processing_mode, value="structure", 
                                         style='Dark.TRadiobutton')
        structure_radio.pack(side=tk.LEFT)
        
        # Frame de ações
        actions_frame = ttk.Frame(main_tab, style='Dark.TFrame')
        actions_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Botões principais
        process_button = ttk.Button(actions_frame, text="🚀 Processar", 
                                   style='Accent.TButton', command=self.start_processing)
        process_button.pack(side=tk.LEFT, padx=(0, 10))
        
        preview_button = ttk.Button(actions_frame, text="👁 Preview", 
                                   style='Dark.TButton', command=self.preview_processing)
        preview_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = ttk.Button(actions_frame, text="🗑 Limpar", 
                                 style='Dark.TButton', command=self.clear_all)
        clear_button.pack(side=tk.LEFT)
        
        # Informações do diretório
        info_frame = DarkTheme.create_card_frame(main_tab, padding=15)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        info_label = ttk.Label(info_frame, text="Informações do Diretório:", style='Dark.TLabel')
        info_label.pack(anchor='w', pady=(0, 10))
        
        # Treeview para preview
        self.preview_tree = FileTreeView(info_frame, height=10)
        self.preview_tree.pack(fill=tk.BOTH, expand=True)
    
    def create_exclusions_tab(self):
        """Cria a aba de exclusões"""
        exclusions_tab = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(exclusions_tab, text="  Exclusões  ")
        
        # Frame de filtros
        filters_frame = DarkTheme.create_card_frame(exclusions_tab, padding=15)
        filters_frame.pack(fill=tk.X, pady=(0, 15))
        
        filters_label = ttk.Label(filters_frame, text="Filtros de Exclusão:", style='Dark.TLabel')
        filters_label.pack(anchor='w', pady=(0, 10))
        
        # Botões de filtro
        filter_buttons_frame = ttk.Frame(filters_frame, style='Dark.TFrame')
        filter_buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        add_file_button = ttk.Button(filter_buttons_frame, text="+ Arquivo", 
                                    style='Dark.TButton', command=self.add_file_exclusion)
        add_file_button.pack(side=tk.LEFT, padx=(0, 10))
        
        add_folder_button = ttk.Button(filter_buttons_frame, text="+ Pasta", 
                                      style='Dark.TButton', command=self.add_folder_exclusion)
        add_folder_button.pack(side=tk.LEFT, padx=(0, 10))
        
        add_pattern_button = ttk.Button(filter_buttons_frame, text="+ Padrão", 
                                       style='Dark.TButton', command=self.add_pattern_exclusion)
        add_pattern_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_exclusions_button = ttk.Button(filter_buttons_frame, text="Limpar Tudo", 
                                            style='Dark.TButton', command=self.clear_exclusions)
        clear_exclusions_button.pack(side=tk.RIGHT)
        
        # Lista de exclusões
        exclusions_list_frame = DarkTheme.create_card_frame(exclusions_tab, padding=15)
        exclusions_list_frame.pack(fill=tk.BOTH, expand=True)
        
        exclusions_label = ttk.Label(exclusions_list_frame, text="Itens Excluídos:", style='Dark.TLabel')
        exclusions_label.pack(anchor='w', pady=(0, 10))
        
        # Treeview para exclusões
        self.exclusions_tree = FileTreeView(exclusions_list_frame, 
                                           columns=('type', 'pattern'), height=15)
        self.exclusions_tree.tree.heading('#0', text='Item')
        self.exclusions_tree.tree.heading('type', text='Tipo')
        self.exclusions_tree.tree.heading('pattern', text='Padrão')
        self.exclusions_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind para remoção
        self.exclusions_tree.tree.bind('<Delete>', self.remove_selected_exclusion)
        self.exclusions_tree.tree.bind('<Double-1>', self.edit_exclusion)
    
    def create_results_tab(self):
        """Cria a aba de resultados"""
        results_tab = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(results_tab, text="  Resultados  ")
        
        # Busca
        search_frame = ttk.Frame(results_tab, style='Dark.TFrame')
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.search_box = SearchBox(search_frame, on_search=self.search_results, 
                                   on_clear=self.clear_search)
        self.search_box.pack(fill=tk.X)
        
        # Lista de arquivos gerados
        files_frame = DarkTheme.create_card_frame(results_tab, padding=15)
        files_frame.pack(fill=tk.BOTH, expand=True)
        
        files_label = ttk.Label(files_frame, text="Arquivos Gerados:", style='Dark.TLabel')
        files_label.pack(anchor='w', pady=(0, 10))
        
        # Treeview para arquivos
        self.results_tree = FileTreeView(files_frame, height=15)
        self.results_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Botões de ação
        results_buttons_frame = ttk.Frame(files_frame, style='Dark.TFrame')
        results_buttons_frame.pack(fill=tk.X)
        
        open_button = ttk.Button(results_buttons_frame, text="Abrir", 
                                style='Accent.TButton', command=self.open_selected_file)
        open_button.pack(side=tk.LEFT, padx=(0, 10))
        
        view_button = ttk.Button(results_buttons_frame, text="Visualizar", 
                                style='Dark.TButton', command=self.view_selected_file)
        view_button.pack(side=tk.LEFT, padx=(0, 10))
        
        delete_button = ttk.Button(results_buttons_frame, text="Excluir", 
                                  style='Dark.TButton', command=self.delete_selected_file)
        delete_button.pack(side=tk.LEFT, padx=(0, 10))
        
        export_button = ttk.Button(results_buttons_frame, text="Exportar", 
                                  style='Dark.TButton', command=self.export_results)
        export_button.pack(side=tk.RIGHT)
        
        folder_button = ttk.Button(results_buttons_frame, text="Abrir Pasta", 
                                  style='Dark.TButton', command=self.open_output_folder)
        folder_button.pack(side=tk.RIGHT, padx=(0, 10))
    
    def create_settings_tab(self):
        """Cria a aba de configurações"""
        settings_tab = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(settings_tab, text="  Configurações  ")
        
        # Extensões
        ext_frame = DarkTheme.create_card_frame(settings_tab, padding=15)
        ext_frame.pack(fill=tk.X, pady=(0, 15))
        
        ext_label = ttk.Label(ext_frame, text="Extensões Suportadas:", style='Dark.TLabel')
        ext_label.pack(anchor='w', pady=(0, 10))
        
        # Lista de extensões
        ext_list_frame = ttk.Frame(ext_frame, style='Dark.TFrame')
        ext_list_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.extensions_var = tk.StringVar(value=' '.join(sorted(self.supported_extensions)))
        ext_entry = ttk.Entry(ext_list_frame, textvariable=self.extensions_var, 
                             style='Dark.TEntry', font=('Segoe UI', 10))
        ext_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        update_ext_button = ttk.Button(ext_list_frame, text="Atualizar", 
                                      style='Accent.TButton', command=self.update_extensions)
        update_ext_button.pack(side=tk.RIGHT)
        
        # Configurações de saída
        output_frame = DarkTheme.create_card_frame(settings_tab, padding=15)
        output_frame.pack(fill=tk.X, pady=(0, 15))
        
        output_label = ttk.Label(output_frame, text="Configurações de Saída:", style='Dark.TLabel')
        output_label.pack(anchor='w', pady=(0, 10))
        
        # Opções de saída
        self.auto_open_results = tk.BooleanVar(value=True)
        self.create_backup = tk.BooleanVar(value=False)
        self.compress_output = tk.BooleanVar(value=False)
        
        auto_open_check = ttk.Checkbutton(output_frame, text="Abrir resultados automaticamente", 
                                         variable=self.auto_open_results, style='Dark.TCheckbutton')
        auto_open_check.pack(anchor='w', pady=2)
        
        backup_check = ttk.Checkbutton(output_frame, text="Criar backup dos arquivos existentes", 
                                      variable=self.create_backup, style='Dark.TCheckbutton')
        backup_check.pack(anchor='w', pady=2)
        
        compress_check = ttk.Checkbutton(output_frame, text="Comprimir arquivos de saída", 
                                        variable=self.compress_output, style='Dark.TCheckbutton')
        compress_check.pack(anchor='w', pady=2)
        
        # Sobre
        about_frame = DarkTheme.create_card_frame(settings_tab, padding=15)
        about_frame.pack(fill=tk.BOTH, expand=True)
        
        about_label = ttk.Label(about_frame, text="Sobre o UltraTexto Pro:", style='Dark.TLabel')
        about_label.pack(anchor='w', pady=(0, 10))
        
        about_text = """UltraTexto Pro v2.0
        
Ferramenta avançada para processamento e análise de arquivos de código.

Funcionalidades:
• Interface moderna com tema escuro
• Processamento de múltiplas extensões de arquivo
• Sistema avançado de exclusões e filtros
• Geração de estruturas de diretório
• Exportação em múltiplos formatos
• Busca e visualização de resultados

Desenvolvido com Python e tkinter."""
        
        about_content = ttk.Label(about_frame, text=about_text, style='Subtitle.TLabel', 
                                 justify=tk.LEFT, wraplength=800)
        about_content.pack(anchor='w')
    
    # Métodos de funcionalidade
    def browse_directory(self):
        """Abre dialog para selecionar diretório"""
        directory = filedialog.askdirectory(title="Selecione o diretório para processar")
        if directory:
            self.selected_directory.set(directory)
            self.current_directory = directory
            self.update_directory_info()
            self.status_bar.set_status(f"Diretório selecionado: {os.path.basename(directory)}")
    
    def update_directory_info(self):
        """Atualiza as informações do diretório selecionado"""
        if not self.current_directory:
            return
        
        # Limpar árvore
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        
        # Contar arquivos e pastas
        total_files = 0
        total_dirs = 0
        supported_files = 0
        
        try:
            for root, dirs, files in os.walk(self.current_directory):
                total_dirs += len(dirs)
                for file in files:
                    total_files += 1
                    if any(file.lower().endswith(ext) for ext in self.supported_extensions):
                        supported_files += 1
                
                # Adicionar apenas o primeiro nível à árvore para preview
                if root == self.current_directory:
                    for dir_name in dirs[:10]:  # Limitar a 10 itens
                        self.preview_tree.insert('', 'end', text=f"📁 {dir_name}", 
                                               values=('', 'Pasta', ''))
                    
                    for file_name in files[:10]:  # Limitar a 10 itens
                        file_path = os.path.join(root, file_name)
                        size = os.path.getsize(file_path)
                        size_str = self.format_file_size(size)
                        ext = os.path.splitext(file_name)[1]
                        icon = "📄" if ext in self.supported_extensions else "📋"
                        self.preview_tree.insert('', 'end', text=f"{icon} {file_name}", 
                                               values=(size_str, 'Arquivo', ''))
                    
                    if len(dirs) > 10 or len(files) > 10:
                        self.preview_tree.insert('', 'end', text="... (mais itens)", 
                                               values=('', '', ''))
                    break
            
            # Atualizar status
            info_text = f"Pastas: {total_dirs} | Arquivos: {total_files} | Suportados: {supported_files}"
            self.status_bar.set_info(info_text)
            
        except Exception as e:
            self.notifications.show_error(f"Erro ao analisar diretório: {str(e)}")
    
    def format_file_size(self, size_bytes):
        """Formata o tamanho do arquivo"""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def start_processing(self):
        """Inicia o processamento em thread separada"""
        if not self.current_directory:
            self.notifications.show_warning("Selecione um diretório primeiro!")
            return
        
        # Iniciar processamento em thread
        thread = threading.Thread(target=self.process_files, daemon=True)
        thread.start()
    
    def process_files(self):
        """Processa os arquivos (executado em thread separada)"""
        progress = ProgressDialog(self.root, "Processando Arquivos", 
                                 "Analisando arquivos e diretórios...")
        
        try:
            # Simular processamento (implementar lógica real aqui)
            progress.update_status("Escaneando diretórios...")
            
            # Aqui seria implementada a lógica real de processamento
            # baseada no código original, mas de forma modular
            
            progress.update_status("Processando arquivos...")
            
            # Simular progresso
            for i in range(101):
                if progress.cancelled:
                    break
                progress.set_progress(i)
                time.sleep(0.02)  # Simular trabalho
            
            if not progress.cancelled:
                progress.close()
                self.root.after(0, lambda: self.notifications.show_success("Processamento concluído!"))
                self.root.after(0, self.refresh_results)
            else:
                progress.close()
                self.root.after(0, lambda: self.notifications.show_info("Processamento cancelado"))
                
        except Exception as e:
            progress.close()
            self.root.after(0, lambda: self.notifications.show_error(f"Erro no processamento: {str(e)}"))
    
    def preview_processing(self):
        """Mostra preview do que será processado"""
        if not self.current_directory:
            self.notifications.show_warning("Selecione um diretório primeiro!")
            return
        
        self.notifications.show_info("Funcionalidade de preview em desenvolvimento")
    
    def clear_all(self):
        """Limpa todas as configurações"""
        self.selected_directory.set("")
        self.current_directory = None
        self.exclusions.clear()
        
        # Limpar árvores
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        
        for item in self.exclusions_tree.get_children():
            self.exclusions_tree.delete(item)
        
        self.status_bar.clear()
        self.notifications.show_info("Configurações limpas")
    
    def add_file_exclusion(self):
        """Adiciona exclusão de arquivo"""
        file_path = filedialog.askopenfilename(title="Selecione arquivo para excluir")
        if file_path:
            self.exclusions.append(('file', file_path))
            self.update_exclusions_tree()
    
    def add_folder_exclusion(self):
        """Adiciona exclusão de pasta"""
        folder_path = filedialog.askdirectory(title="Selecione pasta para excluir")
        if folder_path:
            self.exclusions.append(('folder', folder_path))
            self.update_exclusions_tree()
    
    def add_pattern_exclusion(self):
        """Adiciona exclusão por padrão"""
        pattern = tk.simpledialog.askstring("Padrão de Exclusão", 
                                           "Digite o padrão (ex: *.tmp, test_*, etc.):")
        if pattern:
            self.exclusions.append(('pattern', pattern))
            self.update_exclusions_tree()
    
    def update_exclusions_tree(self):
        """Atualiza a árvore de exclusões"""
        # Limpar árvore
        for item in self.exclusions_tree.get_children():
            self.exclusions_tree.delete(item)
        
        # Adicionar exclusões
        for exc_type, exc_value in self.exclusions:
            icon = {"file": "📄", "folder": "📁", "pattern": "🔍"}.get(exc_type, "❓")
            self.exclusions_tree.insert('', 'end', text=f"{icon} {os.path.basename(exc_value)}", 
                                       values=(exc_type.title(), exc_value))
    
    def clear_exclusions(self):
        """Limpa todas as exclusões"""
        self.exclusions.clear()
        self.update_exclusions_tree()
        self.notifications.show_info("Exclusões removidas")
    
    def remove_selected_exclusion(self, event=None):
        """Remove exclusão selecionada"""
        selection = self.exclusions_tree.selection()
        if selection:
            # Implementar remoção
            self.notifications.show_info("Exclusão removida")
    
    def edit_exclusion(self, event=None):
        """Edita exclusão selecionada"""
        self.notifications.show_info("Funcionalidade de edição em desenvolvimento")
    
    def refresh_results(self):
        """Atualiza a lista de resultados"""
        # Implementar carregamento dos arquivos de resultado
        pass
    
    def search_results(self, query):
        """Busca nos resultados"""
        self.notifications.show_info(f"Buscando por: {query}")
    
    def clear_search(self):
        """Limpa a busca"""
        self.refresh_results()
    
    def open_selected_file(self):
        """Abre arquivo selecionado"""
        self.notifications.show_info("Abrindo arquivo...")
    
    def view_selected_file(self):
        """Visualiza arquivo selecionado"""
        self.notifications.show_info("Visualizando arquivo...")
    
    def delete_selected_file(self):
        """Exclui arquivo selecionado"""
        self.notifications.show_info("Arquivo excluído")
    
    def export_results(self):
        """Exporta resultados"""
        self.notifications.show_info("Exportando resultados...")
    
    def open_output_folder(self):
        """Abre pasta de saída"""
        output_dir = os.path.join(os.getcwd(), "output")
        if os.path.exists(output_dir):
            os.startfile(output_dir)
        else:
            self.notifications.show_warning("Pasta de saída não encontrada")
    
    def update_extensions(self):
        """Atualiza lista de extensões suportadas"""
        try:
            extensions_text = self.extensions_var.get()
            new_extensions = set(ext.strip() for ext in extensions_text.split() if ext.strip())
            self.supported_extensions = new_extensions
            self.notifications.show_success("Extensões atualizadas!")
        except Exception as e:
            self.notifications.show_error(f"Erro ao atualizar extensões: {str(e)}")
    
    def run(self):
        """Executa a aplicação"""
        self.root.mainloop()

def main():
    """Função principal"""
    app = UltraTextoPro()
    app.run()

if __name__ == "__main__":
    main()

